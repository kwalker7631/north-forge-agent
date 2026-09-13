"""Tests for scripts/build-handoff-bundle.ps1 - specifically the fix for the
missing-standalone-report handoff gap: the owner repeatedly uploaded only the
zip to the primary GPT and forgot the separate standalone session report,
so the actual findings never arrived. The zip still must never contain the
current session's own report (the original self-hash-impossibility fix);
this only adds copying that report next to the zip + an explicit reminder.
"""
from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build-handoff-bundle.ps1"
_WINDOWS_ONLY = pytest.mark.skipif(sys.platform != "win32", reason="drives a real .ps1")


def _run(session_report_path: Path, drive_root: Path, sources: list[Path] | None = None):
    args = [
        "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(_SCRIPT),
        "-SessionReportPath", str(session_report_path),
        "-DriveRoot", str(drive_root),
    ]
    if sources:
        args += ["-Sources"] + [str(s) for s in sources]
    return subprocess.run(args, capture_output=True, text=True)


@_WINDOWS_ONLY
def test_report_copied_alongside_the_zip(tmp_path):
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    report = logs_dir / "MY_REPORT_2026-09-12.md"
    report.write_text("RUN-2026-09-12-999: findings go here.\n", encoding="utf-8")
    drive_root = tmp_path / "drive"
    drive_root.mkdir()

    r = _run(report, drive_root)
    assert r.returncode == 0, r.stdout + r.stderr

    copied = drive_root / report.name
    assert copied.exists(), "report was not copied next to the zip"
    assert copied.read_text(encoding="utf-8") == report.read_text(encoding="utf-8")


@_WINDOWS_ONLY
def test_zip_still_never_contains_the_session_report(tmp_path):
    """Regression guard for the original fix this script exists for - copying
    the report next to the zip must not become copying it INTO the zip."""
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    report = logs_dir / "MY_REPORT_2026-09-12.md"
    report.write_text("RUN-2026-09-12-999: findings go here.\n", encoding="utf-8")
    drive_root = tmp_path / "drive"
    drive_root.mkdir()
    prior = tmp_path / "PRIOR_2026-09-11.md"
    prior.write_text("prior session content\n", encoding="utf-8")

    r = _run(report, drive_root, sources=[prior])
    assert r.returncode == 0, r.stdout + r.stderr

    zips = list(drive_root.glob("HANDOFF_*.zip"))
    assert len(zips) == 1
    with zipfile.ZipFile(zips[0]) as zf:
        names = zf.namelist()
    assert report.name not in names
    assert "PRIOR_2026-09-11.md" in names
    assert "HANDOFF-INDEX.md" in names


@_WINDOWS_ONLY
def test_no_copy_error_when_report_already_at_drive_root(tmp_path):
    """The report might already be written directly at -DriveRoot (source and
    destination are the same path) - must not error trying to copy a file
    onto itself."""
    drive_root = tmp_path / "drive"
    drive_root.mkdir()
    report = drive_root / "MY_REPORT_2026-09-12.md"
    report.write_text("RUN-2026-09-12-999: findings go here.\n", encoding="utf-8")

    r = _run(report, drive_root)
    assert r.returncode == 0, r.stdout + r.stderr
    assert report.exists()
    assert report.read_text(encoding="utf-8") == "RUN-2026-09-12-999: findings go here.\n"


@_WINDOWS_ONLY
def test_prints_explicit_both_files_reminder_with_real_names(tmp_path):
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    report = logs_dir / "MY_REPORT_2026-09-12.md"
    report.write_text("RUN-2026-09-12-999: findings go here.\n", encoding="utf-8")
    drive_root = tmp_path / "drive"
    drive_root.mkdir()

    r = _run(report, drive_root)
    assert r.returncode == 0, r.stdout + r.stderr

    out = r.stdout
    assert "IMPORTANT: attach BOTH files" in out
    assert report.name in out
    zips = list(drive_root.glob("HANDOFF_*.zip"))
    assert len(zips) == 1
    assert zips[0].name in out


@_WINDOWS_ONLY
def test_overwrites_a_stale_copy_left_at_drive_root(tmp_path):
    """A same-named leftover from a prior session (same-day reports are often
    named by date, not time) must be replaced with the current content, not
    left stale or refused. Pre-seeds the destination directly rather than
    running the script twice, since two runs in the same wall-clock minute
    would collide on the zip's own minute-precision filename - an unrelated,
    pre-existing constraint of this script, not what this test is checking."""
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    report = logs_dir / "MY_REPORT_2026-09-12.md"
    report.write_text("second, updated version\n", encoding="utf-8")
    drive_root = tmp_path / "drive"
    drive_root.mkdir()
    (drive_root / report.name).write_text("stale first version\n", encoding="utf-8")

    r = _run(report, drive_root)
    assert r.returncode == 0, r.stdout + r.stderr

    assert (drive_root / report.name).read_text(encoding="utf-8") == "second, updated version\n"
