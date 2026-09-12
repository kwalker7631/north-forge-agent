"""scripts/nf_sync_cron.py — declarative cron-from-skill-frontmatter sync.

Regression context (2026-09-12): the standalone North Forge launcher used to
self-register a couple of hardcoded cron jobs on every run. When that
launcher was retired in favor of the profile-pack model, nothing replaced
that self-heal step, so scheduled research/brief jobs from skills like
north-forge-hermes-edition's kyocera-research and daily-brief never got
created unless someone manually typed `/cron add` — something a Basic-tier
teammate drive is never expected to do. This is the generic replacement:
any skill can declare its own schedule in SKILL.md frontmatter and this
script keeps the drive's actual cron jobs in sync with it.

These tests exercise `discover_cron_jobs()` and `sync()` directly against a
fake skills directory and a fake `cronjob()` callable — no real HERMES_HOME
or cron backend required.
"""
import json
import textwrap

import pytest

import scripts.nf_sync_cron as nf_sync_cron


def _write_skill(tmp_path, skill_dir, frontmatter_yaml):
    skill_path = tmp_path / skill_dir
    skill_path.mkdir(parents=True)
    (skill_path / "SKILL.md").write_text(
        f"---\n{frontmatter_yaml}\n---\n# {skill_dir}\nbody text\n", encoding="utf-8")
    return skill_path


class FakeCronjob:
    """Stands in for tools.cronjob_tools.cronjob; records calls, returns real-shaped JSON."""

    def __init__(self, existing_names=(), fail_on_create=frozenset(), gateway_running=True):
        self.existing_names = set(existing_names)
        self.fail_on_create = set(fail_on_create)
        self.gateway_running = gateway_running
        self.create_calls = []

    def __call__(self, action, **kwargs):
        if action == "list":
            jobs = [{"name": name} for name in sorted(self.existing_names)]
            return json.dumps({"success": True, "count": len(jobs), "jobs": jobs})
        if action == "create":
            self.create_calls.append(kwargs)
            name = kwargs["name"]
            if name in self.fail_on_create:
                return json.dumps({"success": False, "error": f"boom creating {name}"})
            self.existing_names.add(name)
            payload = {"success": True, "job_id": "abc123", "name": name}
            if not self.gateway_running:
                payload["gateway_running"] = False
                payload["warning"] = (
                    "The Hermes gateway is not running — this job is saved "
                    "but will NOT fire until the gateway is started.")
            return json.dumps(payload)
        raise AssertionError(f"unexpected action {action!r}")


def test_discover_cron_jobs_reads_declared_frontmatter(tmp_path):
    _write_skill(tmp_path, "kyocera-research", textwrap.dedent("""\
        name: kyocera-research
        description: d
        cron:
          - name: nightly-kyocera-research
            schedule: "0 6 * * *"
            prompt: "Run the kyocera-research pass"
        """))
    _write_skill(tmp_path, "no-schedule-skill", "name: no-schedule-skill\ndescription: d")

    jobs = nf_sync_cron.discover_cron_jobs(tmp_path)

    assert len(jobs) == 1
    assert jobs[0]["name"] == "nightly-kyocera-research"
    assert jobs[0]["schedule"] == "0 6 * * *"
    assert jobs[0]["skill"] == "kyocera-research"


def test_discover_cron_jobs_skips_malformed_entries_without_raising(tmp_path):
    _write_skill(tmp_path, "broken-skill", textwrap.dedent("""\
        name: broken-skill
        description: d
        cron:
          - name: missing-schedule-and-prompt
        """))
    _write_skill(tmp_path, "good-skill", textwrap.dedent("""\
        name: good-skill
        description: d
        cron:
          - name: good-job
            schedule: "0 8 * * *"
            prompt: "do it"
        """))

    jobs = nf_sync_cron.discover_cron_jobs(tmp_path)

    assert [j["name"] for j in jobs] == ["good-job"]


def test_sync_creates_only_missing_jobs_and_never_pins_model(tmp_path):
    _write_skill(tmp_path, "kyocera-research", textwrap.dedent("""\
        name: kyocera-research
        description: d
        cron:
          - name: nightly-kyocera-research
            schedule: "0 6 * * *"
            prompt: "Run the kyocera-research pass"
        """))
    _write_skill(tmp_path, "daily-brief", textwrap.dedent("""\
        name: daily-brief
        description: d
        cron:
          - name: daily-kyocera-brief
            schedule: "0 8 * * *"
            prompt: "Run the daily-brief pass"
        """))
    fake = FakeCronjob(existing_names={"daily-kyocera-brief"})  # one already registered

    result = nf_sync_cron.sync(cronjob_fn=fake, skills_dir=tmp_path)

    assert result["created"] == ["nightly-kyocera-research"]
    assert result["skipped"] == ["daily-kyocera-brief"]
    assert result["failed"] == []
    assert len(fake.create_calls) == 1
    call = fake.create_calls[0]
    assert "model" not in call
    assert "provider" not in call


def test_sync_is_idempotent_second_run_creates_nothing(tmp_path):
    _write_skill(tmp_path, "kyocera-research", textwrap.dedent("""\
        name: kyocera-research
        description: d
        cron:
          - name: nightly-kyocera-research
            schedule: "0 6 * * *"
            prompt: "Run the kyocera-research pass"
        """))
    fake = FakeCronjob()

    first = nf_sync_cron.sync(cronjob_fn=fake, skills_dir=tmp_path)
    second = nf_sync_cron.sync(cronjob_fn=fake, skills_dir=tmp_path)

    assert first["created"] == ["nightly-kyocera-research"]
    assert second["created"] == []
    assert second["skipped"] == ["nightly-kyocera-research"]


def test_sync_reports_failures_without_raising(tmp_path):
    _write_skill(tmp_path, "flaky-skill", textwrap.dedent("""\
        name: flaky-skill
        description: d
        cron:
          - name: flaky-job
            schedule: "0 9 * * *"
            prompt: "do it"
        """))
    fake = FakeCronjob(fail_on_create={"flaky-job"})

    result = nf_sync_cron.sync(cronjob_fn=fake, skills_dir=tmp_path)  # must not raise

    assert result["created"] == []
    assert result["failed"] == [{"job": "flaky-job", "error": "boom creating flaky-job"}]


def test_sync_surfaces_gateway_not_running_warning(tmp_path):
    _write_skill(tmp_path, "kyocera-research", textwrap.dedent("""\
        name: kyocera-research
        description: d
        cron:
          - name: nightly-kyocera-research
            schedule: "0 6 * * *"
            prompt: "Run the kyocera-research pass"
        """))
    fake = FakeCronjob(gateway_running=False)

    result = nf_sync_cron.sync(cronjob_fn=fake, skills_dir=tmp_path)

    assert result["created"] == ["nightly-kyocera-research"]
    assert result["gateway_warning"] is not None
    assert "gateway" in result["gateway_warning"].lower()


def test_main_never_raises_even_when_sync_blows_up(monkeypatch, capsys):
    def _boom(cronjob_fn=None):
        raise RuntimeError("HERMES_HOME not set")

    monkeypatch.setattr(nf_sync_cron, "sync", _boom)
    exit_code = nf_sync_cron.main()

    assert exit_code == 0
    assert "WARNING" in capsys.readouterr().out
