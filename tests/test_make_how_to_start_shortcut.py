"""Tests for scripts/make-how-to-start-shortcut.ps1 - the standing, always-
clickable drive-root entry point back to onboarding content (WELCOME.html or
an installed edition's equivalent docs-index page), distinct from
"Start North Forge.lnk". Same self-healing pattern as
make-drive-root-shortcut.ps1: rewritten every launch, never a stale pointer.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "make-how-to-start-shortcut.ps1"


def _run(repo_root: Path, link_dir: Path):
    return subprocess.run(
        [
            "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(_SCRIPT),
            "-RepoRoot", str(repo_root), "-LinkDir", str(link_dir), "-Quiet",
        ],
        capture_output=True, text=True,
    )


@pytest.mark.windows_only
def test_links_directly_to_chassis_level_welcome_html(tmp_path):
    repo = tmp_path / "north-forge-agent"
    repo.mkdir()
    (repo / "WELCOME.html").write_text("<html>hi</html>", encoding="utf-8")
    link_dir = tmp_path / "drive-root"
    link_dir.mkdir()

    r = _run(repo, link_dir)
    assert r.returncode == 0, r.stdout + r.stderr

    link = link_dir / "How To Start.lnk"
    assert link.exists()


@pytest.mark.windows_only
def test_links_to_installed_private_edition_welcome_html(tmp_path):
    repo = tmp_path / "north-forge-agent"
    edition = repo / "private-editions" / "kyocera"
    edition.mkdir(parents=True)
    (edition / "WELCOME.html").write_text("<html>kyocera</html>", encoding="utf-8")
    link_dir = tmp_path / "drive-root"
    link_dir.mkdir()

    r = _run(repo, link_dir)
    assert r.returncode == 0, r.stdout + r.stderr

    link = link_dir / "How To Start.lnk"
    assert link.exists()


@pytest.mark.windows_only
def test_chassis_level_welcome_html_wins_over_private_edition(tmp_path):
    """If somehow both exist, the chassis-root one is checked first - a
    deliberately-placed top-level page should not be shadowed by a private
    edition's own page."""
    repo = tmp_path / "north-forge-agent"
    edition = repo / "private-editions" / "kyocera"
    edition.mkdir(parents=True)
    (repo / "WELCOME.html").write_text("<html>chassis</html>", encoding="utf-8")
    (edition / "WELCOME.html").write_text("<html>kyocera</html>", encoding="utf-8")
    link_dir = tmp_path / "drive-root"
    link_dir.mkdir()

    r = _run(repo, link_dir)
    assert r.returncode == 0, r.stdout + r.stderr
    assert (link_dir / "How To Start.lnk").exists()


@pytest.mark.windows_only
def test_skips_gracefully_when_no_welcome_html_anywhere(tmp_path):
    repo = tmp_path / "north-forge-agent"
    repo.mkdir()
    link_dir = tmp_path / "drive-root"
    link_dir.mkdir()

    r = _run(repo, link_dir)
    assert r.returncode == 0, r.stdout + r.stderr
    assert not (link_dir / "How To Start.lnk").exists()


@pytest.mark.windows_only
def test_removes_stale_shortcut_when_welcome_html_disappears(tmp_path):
    """A previous edition had a WELCOME.html and got linked; that edition is
    later removed/swapped for one with none. The stale .lnk must not survive -
    it would otherwise point at content that no longer exists."""
    repo = tmp_path / "north-forge-agent"
    edition = repo / "private-editions" / "kyocera"
    edition.mkdir(parents=True)
    (edition / "WELCOME.html").write_text("<html>kyocera</html>", encoding="utf-8")
    link_dir = tmp_path / "drive-root"
    link_dir.mkdir()

    r1 = _run(repo, link_dir)
    assert r1.returncode == 0, r1.stdout + r1.stderr
    assert (link_dir / "How To Start.lnk").exists()

    (edition / "WELCOME.html").unlink()
    r2 = _run(repo, link_dir)
    assert r2.returncode == 0, r2.stdout + r2.stderr
    assert not (link_dir / "How To Start.lnk").exists()


@pytest.mark.windows_only
def test_rewritten_every_run_not_left_stale_on_drive_letter_change(tmp_path):
    """Simulates a drive-letter change: RepoRoot moves, LinkDir (standing in for
    the new drive root) is a fresh directory - the shortcut must still be
    written there, same self-healing guarantee as make-drive-root-shortcut.ps1."""
    old_repo = tmp_path / "old-letter" / "north-forge-agent"
    old_edition = old_repo / "private-editions" / "kyocera"
    old_edition.mkdir(parents=True)
    (old_edition / "WELCOME.html").write_text("<html>kyocera</html>", encoding="utf-8")
    old_link_dir = tmp_path / "old-letter"

    r1 = _run(old_repo, old_link_dir)
    assert r1.returncode == 0, r1.stdout + r1.stderr
    assert (old_link_dir / "How To Start.lnk").exists()

    new_repo = tmp_path / "new-letter" / "north-forge-agent"
    new_edition = new_repo / "private-editions" / "kyocera"
    new_edition.mkdir(parents=True)
    (new_edition / "WELCOME.html").write_text("<html>kyocera</html>", encoding="utf-8")
    new_link_dir = tmp_path / "new-letter"

    r2 = _run(new_repo, new_link_dir)
    assert r2.returncode == 0, r2.stdout + r2.stderr
    assert (new_link_dir / "How To Start.lnk").exists()

# Deliberately no test of the no--LinkDir default path here: that default
# resolves to the REAL drive root of whatever machine runs the test (same
# [System.IO.Path]::GetPathRoot() call make-drive-root-shortcut.ps1 already
# relies on) - exercising it for real would write "How To Start.lnk" onto
# this machine's actual C:\/D:\/E:\ root as a side effect of running the test
# suite, which is not an acceptable thing for a test to do. Every test above
# passes an explicit -LinkDir instead, sandboxed under tmp_path. The "lands at
# the drive root, not inside the checkout" guarantee (EXCALIBUR.md's prior bug
# class) is verified empirically against the real target drive as part of an
# actual drive build, not here.
