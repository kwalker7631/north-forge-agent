# North-Forge Report Manifest

The index the completeness check uses. **Every `RUN-YYYY-MM-DD-NNN` id that
appears anywhere in this ledger must have exactly one row below.** A row either
names a session report that exists in the handoff out-dir (`D:\logs\` — the
`<OutDir>` `scripts/collect-logs.{ps1,sh}` builds) **and** mentions that run id,
or declares the run `ledger-only` (it legitimately produced no report).

`scripts/lib/report_completeness.py` (invoked by both collectors) enforces this:

| Condition | Result |
| --- | --- |
| a ledger `RUN-` id with **no row** here | **FAIL** |
| a row names a report **not present** in the out-dir | **FAIL** |
| the report exists but does **not mention** its run id | **FAIL** |
| a row's `sha256` != the report on disk (report edited) | WARN — refresh the row |
| a row for a `RUN-` id no ledger entry uses | WARN — stale row |
| an unresolved `[[wiki-link]]` in the ledger | WARN — confirm it's intentional |
| a row with no report file, `Source-Of-Truth` citing `lost` | WARN — confirmed unrecoverable, cited, not fabricated |

**Append-only in spirit.** Correct a wrong row by editing it in place (and
refreshing its `sha256`); never delete a row for a run that still exists in the
ledger. Reports dated `2026-09-07` and earlier were written before the
`Run:`/`Covers:`/`Source-Of-Truth:` header convention (`CHG-2026-09-08-008`); they
carry their run id in the body, which is what the check verifies. New reports use
`templates/SESSION-REPORT-TEMPLATE.md`.

`Source-Of-Truth` = `in-bundle` when the `D:\logs\` file *is* the authoritative
write-up; an absolute path / URL when that file is a redacted mirror of a fuller
report kept elsewhere; `ledger-only` when the run produced no report; `lost —
<what happened, cited>` when a report *was* produced (source was `in-bundle`,
its only copy) but that copy was later destroyed by a documented event — never
write bare `lost`, and never use this to paper over a report that simply wasn't
written. **All 30 `lost` rows below (`RUN-2026-09-06-001` through
`RUN-2026-09-11-002`) cite the same event**: `D:\` was wiped and both repos
re-cloned some time before `RUN-2026-09-12-001` — the wipe itself is recorded
after the fact at `CHANGELOG.md`'s `RUN-2026-09-11-001` entry ("re-added the
`upstream` remote (lost when `D:` was wiped and re-cloned)"), and confirmed
empirically this session (2026-09-12): none of the 30 named report files exist
anywhere on `D:\`, in `Downloads\`, or inside any `*.zip` on either location
(handoff bundles included) — checked by filename, not assumed. These reports
had no other Source-Of-Truth to fall back on precisely because `in-bundle`
meant `D:\logs\` was the only copy; the wipe took them all in one event, which
is also why they cluster into one contiguous run rather than being scattered.

To refresh a `sha256` after editing a report:
`python -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" D:\logs\<file>`

---

| RUN id | Report file (in `D:\logs\`) | Covers | Source-Of-Truth | sha256 |
| --- | --- | --- | --- | --- |
| RUN-2026-09-06-001 | — | ledger-schema v2 setup, CHG-2026-09-06-015..019 | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-06-002 | — | CHG-2026-09-06-020, CHG-2026-09-06-021, CHG-2026-09-06-022, CHG-2026-09-06-023, CHG-2026-09-06-024, DECISION-2026-09-06-001 | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-06-003 | — | CHG-2026-09-06-025, CHG-2026-09-06-026 | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-07-001 | — | consolidated pass (step 4 → DECISION-2026-09-06-003 opened) | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-07-002 | — | CHG-2026-09-07-007 | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-07-003 | — | CHG-2026-09-07-009, CHG-2026-09-07-010, ERR-2026-09-07-002 | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-07-004 | — | CHG-2026-09-07-011, CHG-2026-09-07-012, CHG-2026-09-07-013, CHG-2026-09-07-014, DECISION-2026-09-07-001 | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-07-005 | — | CHG-2026-09-07-015, ERR-2026-09-07-003 | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-07-006 | — | CHG-2026-09-07-016, CHG-2026-09-07-017, CHG-2026-09-07-018, ERR-2026-09-07-004, ERR-2026-09-07-006, ERR-2026-09-07-007, DECISION-2026-09-07-002 | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-07-007 | — | CHG-2026-09-07-019, ERR-2026-09-07-005 | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-07-008 | — | CHG-2026-09-07-020, ERR-2026-09-07-006 | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-07-009 | — | CHG-2026-09-07-021 | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-07-010 | — | CHG-2026-09-07-022, DECISION-2026-09-07-003 | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-07-011 | — | CHG-2026-09-07-023, DECISION-2026-09-06-002, DECISION-2026-09-06-003 | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-08-001 | — | CHG-2026-09-08-001, CHG-2026-09-08-002, CHG-2026-09-08-003, CHG-2026-09-08-004 | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-08-002 | — | CHG-2026-09-08-005 | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-08-003 | — | CHG-2026-09-08-006, CHG-2026-09-08-007 | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-08-004 | — | CHG-2026-09-08-008, CHG-2026-09-08-009, CHG-2026-09-08-010, CHG-2026-09-08-011, CHG-2026-09-08-012, CHG-2026-09-08-013, CHG-2026-09-08-014, CHG-2026-09-08-015, CHG-2026-09-08-016, ERR-2026-09-07-004, ERR-2026-09-07-007, ERR-2026-09-08-001, ERR-2026-09-08-002, ERR-2026-09-08-003, ERR-2026-09-08-004, DECISION-2026-09-07-002 | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-08-005 | — | CHG-2026-09-08-017, CHG-2026-09-08-018, CHG-2026-09-08-019, CHG-2026-09-08-020, CHG-2026-09-08-021, CHG-2026-09-08-022, CHG-2026-09-08-023, CHG-2026-09-08-024, CHG-2026-09-08-025, ERR-2026-09-08-005, ERR-2026-09-08-006, ERR-2026-09-08-007, ERR-2026-09-08-008, ERR-2026-09-08-009, ERR-2026-09-08-010, ERR-2026-09-08-011, ERR-2026-09-08-012 | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-09-001 | — | CHG-2026-09-09-001, CHG-2026-09-09-002, ERR-2026-09-09-001, ERR-2026-09-09-002, ERR-2026-09-09-003 | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-09-002 | — | DECISION-2026-09-09-001, CHG-2026-09-09-003 | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-10-001 | — | CHG-2026-09-10-001, DECISION-2026-09-10-001, ERR-2026-09-10-001 | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-10-002 | — | CHG-2026-09-10-002, ERR-2026-09-10-001 | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-10-003 | — | CHG-2026-09-10-003, CHG-2026-09-10-004, ERR-2026-09-10-001 | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-10-004 | — | — (no CHG/ERR/DECISION; investigation + drive cleanup only) | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-10-005 | — | — (no CHG/ERR/DECISION; investigation only, no changes) | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-10-006 | — | CHG-2026-09-10-005 | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-10-007 | — | — (no CHG/ERR/DECISION; audit found nothing to fix) | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-11-001 | — | CHG-2026-09-11-001, CHG-2026-09-11-002 | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-11-002 | — | CHG-2026-09-11-003, CHG-2026-09-11-004, ERR-2026-09-11-001, DECISION-2026-09-11-001 | lost — D: wipe before RUN-2026-09-12-001, see header note | — |
| RUN-2026-09-12-001 | LEDGER-INDEX-INCIDENT-CLEANUP_2026-09-12.md | CHG-2026-09-12-001 | in-bundle | a804cc880159baea0f359921b510645b106690d8835f8d2ba6c46169d59126f9 |
| RUN-2026-09-12-002 | ARCHITECTURE_PLACEMENT_AND_HANDOFF_FIX_2026-09-12.md | CHG-2026-09-12-002, CHG-2026-09-12-003 | in-bundle | 1322d90b3ecd48059b22a40de9f8728eff05181710fbc372bb4f909977c922cb |
| RUN-2026-09-12-003 | CRON_GATEWAY_VERIFICATION_2026-09-12.md | CHG-2026-09-12-004, CHG-2026-09-12-005, ERR-2026-09-12-001, ERR-2026-09-12-002 | in-bundle | 2d32186e5e051d0775ed4b94a664f935ccce6ddbace0508ed0e615d4f56b240c |
| RUN-2026-09-12-004 | FINAL_PUSH_VERIFICATION_2026-09-12.md | ledger-only (push + verification pass; no new CHG/ERR/DECISION) | in-bundle | c25dc7809cdce7cb3f4cb449e046230ffc2b840b02df883b91561c41bd8ab46d |
| RUN-2026-09-12-005 | REPORT-MANIFEST-COMPLETENESS-FIX_2026-09-12.md | CHG-2026-09-12-006 | in-bundle | a737159391a60bfef42fbfcb66bda078c2532bfe77629eaa6a571b66c1bdda72 |
| RUN-2026-09-12-006 | HOW-TO-START-SHORTCUT_2026-09-12.md | CHG-2026-09-12-007 | in-bundle | — |
