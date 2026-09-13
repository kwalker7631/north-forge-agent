# build-handoff-bundle - builds the session-scoped HANDOFF_<date>_<time>.zip at a drive
# root, cross-linked BY NAME to the current session's own report rather than containing it.
<#
  scripts\build-handoff-bundle.ps1  -SessionReportPath <path>  [-Sources <path[]>]
                                     [-DriveRoot <path>]  [-Label <text>]

  WHAT IT DOES
    Builds  <DriveRoot>\HANDOFF_<yyyy-MM-dd_HHmm>.zip  +  the matching  .zip.sha256
    sidecar, containing ONLY previously-existing artifacts (-Sources: prior session
    reports, CLAUDE_CODE_LAST_AUDIT.md, CODEX_PUSH_LOG.md, forge-events.log,
    install-logs\, or anything else you point it at) plus one generated
    HANDOFF-INDEX.md that names the CURRENT session's own report by path/filename
    and its own real sha256 for cross-reference - it does not copy that report's
    bytes into the zip.

    It ALSO copies -SessionReportPath itself to <DriveRoot>\<same filename> (unless
    it's already sitting there) - see "THE MISSING-REPORT HANDOFF GAP" below - and
    prints an explicit, hard-to-miss final reminder naming both files by their real
    filenames.

  THE MISSING-REPORT HANDOFF GAP (fixed 2026-09-12, CHG-2026-09-12 follow-up)
    The zip deliberately never contains the current session's own report (see WHY,
    below) - it was only ever written to logs\, a different folder from the drive
    root where the zip lands. In practice, the owner repeatedly uploaded only the
    zip to the primary GPT and forgot the separate standalone report sitting
    elsewhere, meaning the actual current findings never arrived, more than once.
    Not a one-time reminder problem - a structural one: two files that must travel
    together lived in two different places. Fix: put them in the same place
    (literally next to each other, at -DriveRoot) and print a reminder naming both
    files explicitly, every run, immediately before the script exits.

  WHY (see logs\ledger\CHANGELOG.md CHG-2026-09-12, "handoff-bundle self-reference"
  and the owner's own follow-up task) -- a report cannot contain the real sha256 of a
  zip that contains that same report: the hash doesn't exist until the zip is sealed,
  so any report embedded in its own bundle is necessarily one revision stale the
  moment you read it back out of the zip. Standalone reports + their .sha256 sidecars
  were always the authoritative copy; this script just stops manufacturing the
  confusing stale copy in the first place by never zipping the current report at all.

  -SessionReportPath is REQUIRED and is used only to compute the cross-reference
  entry (name, sha256, byte size) written into HANDOFF-INDEX.md. If it is
  ALSO present in -Sources (a caller mistake - re-introducing the exact bug this
  script exists to prevent), it is dropped from the staged set and a WARN is
  printed; the run does not fail, but check the output.

  EXIT CODE  0 = zip built (0 or more -Sources existed; missing ones are WARN, not
             fatal - a first-ever run with nothing to carry forward is still valid).
             1 = -SessionReportPath does not exist, or the zip could not be written.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SessionReportPath,
    [string[]]$Sources = @(),
    [string]$DriveRoot,
    [string]$Label = ''
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $SessionReportPath)) {
    Write-Error "SessionReportPath '$SessionReportPath' does not exist."
    exit 1
}
$SessionReportPath = (Resolve-Path -LiteralPath $SessionReportPath).Path
$sessionReportName = Split-Path -Leaf $SessionReportPath

if (-not $DriveRoot) {
    # Split-Path -Qualifier returns a bare "D:" with no trailing separator, which
    # Windows treats as DRIVE-RELATIVE (relative to that drive's current working
    # directory), not drive-ROOTED - Resolve-Path on it silently resolved to
    # wherever the process happened to be cd'd on that drive instead of the
    # actual root, so the bundle landed inside a repo checkout instead of at the
    # drive root. Appending the separator forces the rooted interpretation.
    $DriveRoot = (Split-Path -Qualifier $SessionReportPath) + '\'
}
if (-not (Test-Path -LiteralPath $DriveRoot)) {
    Write-Error "DriveRoot '$DriveRoot' does not exist."
    exit 1
}
$DriveRoot = (Resolve-Path -LiteralPath $DriveRoot).Path.TrimEnd('\')

$stamp    = Get-Date
$stampTag = $stamp.ToString('yyyy-MM-dd_HHmm')
$zipPath  = Join-Path $DriveRoot "HANDOFF_$stampTag.zip"
$shaPath  = "$zipPath.sha256"

function Get-Sha256Hex([string]$path) {
    return (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLower()
}

# --- resolve -Sources: drop anything that doesn't exist (WARN), drop the current
# report itself if a caller mistakenly included it (WARN, guards the exact bug this
# script fixes), dedupe. ---------------------------------------------------------
$staged = New-Object System.Collections.Generic.List[string]
$warnings = New-Object System.Collections.Generic.List[string]
foreach ($raw in $Sources) {
    if ([string]::IsNullOrWhiteSpace($raw)) { continue }
    if (-not (Test-Path -LiteralPath $raw)) {
        $warnings.Add("source not found, skipped: $raw")
        continue
    }
    $resolved = (Resolve-Path -LiteralPath $raw).Path
    if ($resolved -ieq $SessionReportPath) {
        $warnings.Add("SessionReportPath was also passed in -Sources ($raw) - dropped. " +
            "The whole point of this script is that the current session's own report " +
            "is never bundled into its own zip; pass only PREVIOUS sessions' artifacts.")
        continue
    }
    if (-not $staged.Contains($resolved)) { $staged.Add($resolved) }
}

# --- stage into a throwaway temp dir, zip, hash --------------------------------
$stageDir = Join-Path $env:TEMP "handoff_stage_$stampTag"
if (Test-Path -LiteralPath $stageDir) { $stageDir = "$stageDir`_$([guid]::NewGuid().ToString('N').Substring(0,6))" }
New-Item -ItemType Directory -Path $stageDir -Force | Out-Null

$includedNames = New-Object System.Collections.Generic.List[string]
foreach ($src in $staged) {
    $item = Get-Item -LiteralPath $src
    if ($item.PSIsContainer) {
        Copy-Item -LiteralPath $src -Destination (Join-Path $stageDir $item.Name) -Recurse -Force
    } else {
        Copy-Item -LiteralPath $src -Destination (Join-Path $stageDir $item.Name) -Force
    }
    $includedNames.Add($item.Name)
}

$reportSha  = Get-Sha256Hex $SessionReportPath
$reportSize = (Get-Item -LiteralPath $SessionReportPath).Length
$indexLines = @(
    "# Handoff bundle index"
    ""
    "Built: $($stamp.ToString('yyyy-MM-dd HH:mm:ss zzz'))"
    ($(if ($Label) { "Label: $Label" } else { $null }))
    ""
    "## Accompanying session report (delivered STANDALONE, not inside this zip)"
    ""
    "- Name: ``$sessionReportName``"
    "- Path at build time: ``$SessionReportPath``"
    "- Size: $reportSize bytes"
    "- sha256: ``$reportSha``"
    ""
    "This bundle deliberately does NOT contain the file above. See CHG-2026-09-12 in"
    "logs\ledger\CHANGELOG.md for why: a file cannot contain the real hash of a zip"
    "that contains that same file. The report's own closing 'Handoff bundle:' line"
    "names this zip and this zip's own sha256 (in the sidecar next to it), and that"
    "line is filled in AFTER this zip is sealed - so it is always correct, never a"
    "stale pre-seal snapshot."
    ""
    "## Contents of this zip (previous sessions' artifacts only)"
    ""
) | Where-Object { $null -ne $_ }
if ($includedNames.Count -eq 0) {
    $indexLines += "_(none - no -Sources existed or were given this run.)_"
} else {
    foreach ($n in $includedNames) { $indexLines += "- ``$n``" }
}
if ($warnings.Count -gt 0) {
    $indexLines += ""
    $indexLines += "## Warnings"
    $indexLines += ""
    foreach ($w in $warnings) { $indexLines += "- $w" }
}
[System.IO.File]::WriteAllText(
    (Join-Path $stageDir 'HANDOFF-INDEX.md'),
    (($indexLines -join "`n") -replace "`r`n", "`n"),
    (New-Object System.Text.UTF8Encoding($false))
)

if (Test-Path -LiteralPath $zipPath) {
    Write-Error "$zipPath already exists (two runs in the same minute?) - not overwriting; pick a different moment or remove it first."
    exit 1
}
Compress-Archive -Path (Join-Path $stageDir '*') -DestinationPath $zipPath
$zipSha = Get-Sha256Hex $zipPath
[System.IO.File]::WriteAllText($shaPath, $zipSha, (New-Object System.Text.UTF8Encoding($false)))

# --- copy the current session's own report next to the zip, not just logs\ ----
# This is the actual fix for the missing-report handoff gap: both files now sit
# in the same folder, so grabbing one without seeing the other takes an extra,
# deliberate step instead of being the easy default.
$reportDestPath = Join-Path $DriveRoot $sessionReportName
$reportCopied = $false
if ($reportDestPath -ieq $SessionReportPath) {
    # Already sitting at -DriveRoot (e.g. the report was written there directly) -
    # nothing to copy, not an error.
} else {
    Copy-Item -LiteralPath $SessionReportPath -Destination $reportDestPath -Force
    $reportCopied = $true
}

foreach ($w in $warnings) { Write-Warning $w }
Write-Host ""
Write-Host "Built $zipPath" -ForegroundColor Green
Write-Host "  sha256: $zipSha"
Write-Host "  contains: $($includedNames.Count) item(s) from -Sources + HANDOFF-INDEX.md"
Write-Host "  does NOT contain: $sessionReportName (the current session's own report - delivered standalone)"
if ($reportCopied) {
    Write-Host "  report copied alongside it: $reportDestPath"
} else {
    Write-Host "  report already alongside it: $reportDestPath"
}
Write-Host ""
Write-Host "Fill this line into the standalone report's closing line:" -ForegroundColor Cyan
Write-Host "  Handoff bundle: HANDOFF_$stampTag.zip (sha256: $zipSha) - created."
Write-Host ""
Write-Host "================================================================" -ForegroundColor Yellow
Write-Host "IMPORTANT: attach BOTH files when sending to the primary GPT:" -ForegroundColor Yellow
Write-Host "  1. $(Split-Path -Leaf $zipPath)" -ForegroundColor Yellow
Write-Host "  2. $sessionReportName  <-- the actual findings are in this one" -ForegroundColor Yellow
Write-Host "  Both are now sitting together in: $DriveRoot" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Yellow

exit 0
