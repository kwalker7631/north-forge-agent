#!/usr/bin/env python3
"""Sync declarative cron jobs from installed skills' SKILL.md frontmatter.

Problem this closes: skills used to rely on someone manually typing
`/cron add ...` inside a live interactive session to get their scheduled jobs
registered. The old standalone North Forge launcher used to paper over that
by self-registering a couple of hardcoded jobs on every launch; when this
chassis stopped shipping its own launcher (profile-pack model, see
editions/README.md), that self-heal step had nothing to replace it, so a
freshly provisioned drive — Basic tier especially, since those users are not
expected to type CLI commands at all — never got its research/brief jobs
scheduled. See north-forge-hermes-edition's kyocera-research and daily-brief
skills for the motivating case.

The fix: any installed skill can declare its own schedule directly in its
SKILL.md frontmatter —

    ---
    name: my-skill
    description: ...
    cron:
      - name: my-nightly-job       # required, used as the idempotency key
        schedule: "0 6 * * *"      # required, cron expression
        prompt: "Do the thing"     # required unless the job is skill-only
        skill: my-skill            # optional, defaults to this SKILL.md's own name
        skills: []                 # optional, additional skills to attach
    ---

This script walks every skill under SKILLS_DIR, collects those blocks, and
calls the same `tools.cronjob_tools.cronjob()` Python API the CLI/agent uses
to create any job that is missing by name — never touching jobs that already
exist (so a user's own edits to schedule/prompt after creation are never
clobbered) and never passing model/provider, so each job inherits whatever
this drive's own cron/model default already is. That last part is what makes
this behave identically on Basic and Full tier: a Basic drive's default model
is exactly what a job created here will run on, with no separate code path.

Registering a job is necessary but not sufficient: the cron ticker lives in
the Hermes gateway process, so a job sits inert until something is actually
running to fire it. This used to be left as a manual step ("run `hermes
gateway install` yourself"). It no longer is: whenever at least one skill
declares a cron job, this script also calls `hermes_cli.gateway
.ensure_gateway_service()` — the same zero-prompt, never-raising install path
`hermes setup`/`hermes import` already use internally. It short-circuits True
if a gateway is already running, installs a user-scope systemd/launchd/
Windows-Scheduled-Task service and starts it when nothing is installed yet,
and just starts an already-installed-but-stopped one. It no-ops safely (with
its own explanatory message) inside containers and on hosts with no service
manager at all, where a restart policy or `hermes gateway run` is the right
answer instead of a background service — so this script never fights either
of those cases.

Meant to be cheap, idempotent, and non-fatal: called from north-forge.cmd's
self-healing block on every launch, and once at the end of nf-setup.ps1 right
after provisioning, so a fresh Basic-tier drive has its jobs registered — and
a gateway installed and running to fire them — before anyone opens an
interactive session at all. A failure at any step here must never block a
launch — print a warning (mirroring the old launcher's on-screen
CRON_DEGRADED behavior) and move on.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterator, List


def _read_frontmatter(skill_md: str) -> dict:
    """YAML frontmatter of a SKILL.md body ({} when absent/invalid).

    Mirrors hermes_cli/skills_hub.py's own `_read_frontmatter` byte-for-byte
    so the two never silently diverge on what counts as valid frontmatter.
    """
    import yaml
    match = re.search(r'\n---\s*\n', skill_md[3:]) if skill_md.startswith("---") else None
    try:
        return (yaml.safe_load(skill_md[3:match.start() + 3]) or {}) if match else {}
    except yaml.YAMLError:
        return {}


def discover_cron_jobs(skills_dir: Path) -> List[Dict[str, Any]]:
    """Every well-formed `cron:` entry across every skill under skills_dir.

    Malformed entries (missing name/schedule/prompt, wrong types) are
    skipped with a warning rather than raising — one broken skill must not
    stop every other skill's jobs from syncing.
    """
    jobs: List[Dict[str, Any]] = []
    if not skills_dir.is_dir():
        return jobs
    for skill_md_path in sorted(skills_dir.glob("*/SKILL.md")):
        skill_dir_name = skill_md_path.parent.name
        try:
            body = skill_md_path.read_text(encoding="utf-8").lstrip("\ufeff")
        except OSError as exc:
            print(f"[nf-sync-cron] WARNING: could not read {skill_md_path}: {exc}")
            continue
        frontmatter = _read_frontmatter(body)
        declared = frontmatter.get("cron")
        if declared is None:
            continue
        if not isinstance(declared, list):
            print(f"[nf-sync-cron] WARNING: {skill_dir_name}: 'cron' frontmatter "
                  f"must be a list, skipping")
            continue
        skill_name = frontmatter.get("name", skill_dir_name)
        for entry in declared:
            if not isinstance(entry, dict):
                print(f"[nf-sync-cron] WARNING: {skill_dir_name}: skipping non-mapping "
                      f"cron entry {entry!r}")
                continue
            name, schedule, prompt = entry.get("name"), entry.get("schedule"), entry.get("prompt")
            if not name or not schedule or not prompt:
                print(f"[nf-sync-cron] WARNING: {skill_dir_name}: cron entry missing "
                      f"required name/schedule/prompt, skipping: {entry!r}")
                continue
            primary_skill = entry.get("skill", skill_name)
            extra_skills = entry.get("skills") or []
            # tools.cronjob_tools._canonical_skills() only falls back to the singular
            # `skill=` kwarg when `skills=` is None — an explicit `skills=[]` (which is
            # what `entry.get("skills") or []` used to always produce here) is treated
            # as "no skills at all" and silently drops the primary skill, leaving the
            # persisted job's "skill" field null. Build the combined list ourselves so
            # the primary skill is never lost regardless of that fallback-only quirk.
            combined_skills = ([primary_skill] if primary_skill else []) + [
                s for s in extra_skills if s != primary_skill]
            jobs.append({
                "name": name,
                "schedule": schedule,
                "prompt": prompt,
                "skill": primary_skill,
                "skills": combined_skills or None,
                "_source_skill": skill_dir_name,
            })
    return jobs


def _existing_job_names(cronjob_fn) -> set[str]:
    raw = cronjob_fn(action="list", include_disabled=True)
    try:
        parsed = json.loads(raw)
    except (TypeError, ValueError) as exc:
        raise RuntimeError(f"cronjob(action='list') returned non-JSON: {raw!r}") from exc
    if not parsed.get("success", True):
        raise RuntimeError(f"cronjob(action='list') failed: {parsed.get('error')}")
    return {job.get("name") for job in parsed.get("jobs", []) if job.get("name")}


def sync(cronjob_fn=None, skills_dir: "Path | None" = None) -> Dict[str, Any]:
    """Create every declared job that isn't registered yet.

    `cronjob_fn` and `skills_dir` are injectable for tests; production
    callers leave both None and get the real `tools.cronjob_tools.cronjob`
    and the real, live-resolved `tools.skills_hub.SKILLS_DIR` (imported here,
    not at module load, so a profile override made after this module is
    imported is still honored — same convention skills_hub.py itself uses).
    Deliberately never passes model/provider to create() — see module
    docstring.
    """
    if cronjob_fn is None:
        from tools.cronjob_tools import cronjob as cronjob_fn
    if skills_dir is None:
        from tools.skills_hub import SKILLS_DIR
        skills_dir = Path(SKILLS_DIR)

    result: Dict[str, Any] = {
        "created": [], "skipped": [], "failed": [], "gateway_warning": None, "declared_count": 0,
    }
    declared_jobs = discover_cron_jobs(skills_dir)
    result["declared_count"] = len(declared_jobs)
    if not declared_jobs:
        return result

    try:
        existing = _existing_job_names(cronjob_fn)
    except Exception as exc:  # noqa: BLE001 - never fatal, this is a self-heal step
        print(f"[nf-sync-cron] WARNING: could not list existing cron jobs, "
              f"skipping sync this run: {exc}")
        result["failed"].append({"job": "<list>", "error": str(exc)})
        return result

    for job in declared_jobs:
        if job["name"] in existing:
            result["skipped"].append(job["name"])
            continue
        try:
            raw = cronjob_fn(
                action="create", schedule=job["schedule"], prompt=job["prompt"],
                name=job["name"], skill=job["skill"], skills=job["skills"],
            )
            parsed = json.loads(raw)
            if not parsed.get("success", False):
                raise RuntimeError(parsed.get("error", "unknown error"))
            result["created"].append(job["name"])
            if result["gateway_warning"] is None and parsed.get("gateway_running") is False:
                result["gateway_warning"] = parsed.get(
                    "warning",
                    "cron jobs are registered but no gateway is running to fire them — "
                    "run 'hermes gateway install' so they run unattended.")
        except Exception as exc:  # noqa: BLE001 - one bad job must not block the rest
            print(f"[nf-sync-cron] WARNING: could not schedule '{job['name']}' "
                  f"(from skill '{job['_source_skill']}'): {exc}")
            result["failed"].append({"job": job["name"], "error": str(exc)})
    return result


def ensure_gateway(ensure_fn=None) -> Dict[str, Any]:
    """Best-effort install+start of the Hermes gateway service, so cron jobs
    that are already registered actually fire unattended instead of sitting
    inert until someone remembers to run `hermes gateway install` by hand.

    `ensure_fn` is injectable for tests; production callers leave it None and
    get the real `hermes_cli.gateway.ensure_gateway_service` (imported here,
    not at module load, since that module pulls in the full gateway/CLI
    dependency stack — same lazy-import convention `sync()` uses above).

    Never raises — `ensure_gateway_service` itself already never raises or
    prompts (it's the same zero-prompt path `hermes setup`/`hermes import`
    use), but a failed import of its dependency chain, or a test double that
    misbehaves, is still caught here rather than allowed to propagate.
    Returns {"attempted": bool, "running": bool, "error": str | None}.
    """
    result: Dict[str, Any] = {"attempted": False, "running": False, "error": None}
    if ensure_fn is None:
        try:
            from hermes_cli.gateway import ensure_gateway_service as ensure_fn
        except Exception as exc:  # noqa: BLE001 - optional dependency chain, never fatal
            result["error"] = f"could not load the gateway module: {exc}"
            return result
    result["attempted"] = True
    try:
        result["running"] = bool(ensure_fn(context="nf-sync-cron"))
    except Exception as exc:  # noqa: BLE001 - belt-and-suspenders; see docstring above
        result["error"] = str(exc)
    return result


def main() -> int:
    """CLI entry point for north-forge.cmd / nf-setup.ps1. Always exits 0 —
    a cron-sync problem degrades a feature, it must never fail a launch or a
    provisioning run."""
    try:
        result = sync()
    except Exception as exc:  # noqa: BLE001 - absolute last resort, see docstring above
        print(f"[nf-sync-cron] WARNING: cron sync did not run: {exc}")
        return 0

    if result["created"]:
        print(f"[nf-sync-cron] registered {len(result['created'])} cron job(s): "
              f"{', '.join(result['created'])}")
    if result["failed"]:
        print(f"[nf-sync-cron] WARNING SUMMARY: {len(result['failed'])} job(s) "
              f"could not be scheduled — research/brief automation may be incomplete "
              f"until this is resolved:")
        for failure in result["failed"]:
            print(f"[nf-sync-cron]   - {failure['job']}: {failure['error']}")

    if result.get("declared_count"):
        # At least one skill wants cron capability — make sure something is actually
        # running to fire it, instead of just leaving the old warning on-screen.
        try:
            gw = ensure_gateway()
        except Exception as exc:  # noqa: BLE001 - absolute last resort, see docstring above
            gw = {"attempted": False, "running": False, "error": str(exc)}
        if gw["running"]:
            print("[nf-sync-cron] gateway service confirmed running — scheduled jobs will fire unattended.")
        else:
            reason = gw["error"] or result["gateway_warning"] or "the gateway service is not running yet"
            print(f"[nf-sync-cron] NOTE: {reason}")
            if gw["attempted"]:
                print("[nf-sync-cron]   Automatic install/start did not complete this run — "
                      "retry manually with: hermes gateway install")
    return 0


if __name__ == "__main__":
    sys.exit(main())
