# make-how-to-start-shortcut - (re)generates "<drive root>\How To Start.lnk", a
# double-click launcher distinct from "Start North Forge.lnk" that opens the
# installed edition's WELCOME.html (or an equivalent docs-index page) on demand -
# not just on first launch, and not something you have to remember a filename or
# dig through the checkout folder to find again later.
<#
  scripts\make-how-to-start-shortcut.ps1  [-RepoRoot <path>]  [-LinkDir <path>]
                                          [-LinkName <name.lnk>]  [-Quiet]

  WHY THIS EXISTS
    Before this script, the only onboarding entry point was WELCOME.html itself
    (opened once, historically, by the retired standalone launcher) plus the
    plain-text HOW_TO_START.txt some docs describe - neither is a standing,
    always-clickable way to get back to onboarding content after the first run.
    Same self-healing principle as make-drive-root-shortcut.ps1: this runs on
    EVERY launch (north-forge.cmd calls both), so the drive-root shortcut is
    rewritten from scratch each run against wherever the checkout currently is -
    always correct for the current drive letter, never a stale pointer.

  WHAT IT WRITES
    <LinkDir>\<LinkName>   default:  <root of RepoRoot's drive>\How To Start.lnk
      TargetPath  = the first WELCOME.html found under -RepoRoot (checked, in
                    order: <RepoRoot>\WELCOME.html, then
                    <RepoRoot>\private-editions\*\WELCOME.html) - whichever
                    edition is actually installed, not hardcoded to one name.
      WorkingDirectory = the folder containing that WELCOME.html
      Description = self-identifying, notes it is auto-regenerated

    The generated .lnk is NOT tracked in git (created outside the checkout, at
    the drive root) - a build artifact of running north-forge.cmd, same as
    "Start North Forge.lnk".

  IF NO WELCOME.html EXISTS ANYWHERE UNDER -RepoRoot
    Skip creating the shortcut (best-effort, not fatal) - some future chassis-only
    install may genuinely have no docs-index page yet. Removes any stale .lnk
    left over from a previous edition that DID have one, so a leftover shortcut
    never points at content that's no longer installed.

  PARAMS
    -RepoRoot   the checkout root. Default: the parent of this script's folder.
    -LinkDir    where to write the .lnk. Default: the drive root of -RepoRoot
                (e.g. RepoRoot D:\north-forge-agent -> D:\). Override for tests /
                to simulate a drive-letter change.
    -LinkName   the .lnk filename. Default: "How To Start.lnk".
    -Quiet      suppress the normal one-line status print (errors still print).

  EXIT  0 = shortcut written, refreshed, or intentionally skipped/removed
        (no WELCOME.html found). 1 = found a target but could not write the
        .lnk (COM failure). north-forge.cmd calls this best-effort and ignores
        the exit code so a failure here never blocks the agent from starting.
#>
[CmdletBinding()]
param(
    [string]$RepoRoot,
    [string]$LinkDir,
    [string]$LinkName = "How To Start.lnk",
    [switch]$Quiet
)

$ErrorActionPreference = 'Stop'

function Write-Status([string]$msg) { if (-not $Quiet) { Write-Host "[how-to-start-shortcut] $msg" } }

function Find-WelcomePage([string]$RepoRoot) {
    $direct = Join-Path $RepoRoot 'WELCOME.html'
    if (Test-Path -LiteralPath $direct) { return $direct }

    $privateEditions = Join-Path $RepoRoot 'private-editions'
    if (Test-Path -LiteralPath $privateEditions) {
        $found = Get-ChildItem -LiteralPath $privateEditions -Filter 'WELCOME.html' -Recurse -Depth 2 -ErrorAction SilentlyContinue |
            Select-Object -First 1
        if ($found) { return $found.FullName }
    }
    return $null
}

try {
    if (-not $RepoRoot) { $RepoRoot = Split-Path -Parent $PSScriptRoot }
    $RepoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path.TrimEnd('\')

    if (-not $LinkDir) { $LinkDir = [System.IO.Path]::GetPathRoot($RepoRoot) }
    if (-not $LinkDir) {
        Write-Error "could not determine a drive root for '$RepoRoot'; pass -LinkDir."
        exit 1
    }
    if (-not (Test-Path -LiteralPath $LinkDir)) {
        New-Item -ItemType Directory -Path $LinkDir -Force | Out-Null
    }

    $linkPath = Join-Path $LinkDir $LinkName
    $target = Find-WelcomePage -RepoRoot $RepoRoot

    if (-not $target) {
        if (Test-Path -LiteralPath $linkPath) {
            Remove-Item -LiteralPath $linkPath -Force -ErrorAction SilentlyContinue
            Write-Status "no WELCOME.html found under '$RepoRoot' - removed stale '$linkPath'."
        }
        else {
            Write-Status "no WELCOME.html found under '$RepoRoot' - nothing to link, skipping."
        }
        exit 0
    }

    # Rewrite from scratch every run: drop any prior copy first so a partial/locked
    # file, or one pointing at a previous edition's page, can't leave stale
    # metadata behind.
    if (Test-Path -LiteralPath $linkPath) {
        Remove-Item -LiteralPath $linkPath -Force -ErrorAction SilentlyContinue
    }

    $shell = New-Object -ComObject WScript.Shell
    try {
        $sc = $shell.CreateShortcut($linkPath)
        $sc.TargetPath       = $target
        $sc.WorkingDirectory = Split-Path -Parent $target
        $sc.WindowStyle      = 1
        $sc.Description      = "Open the onboarding / quick-start page. Auto-regenerated by north-forge.cmd on every run - safe to delete."
        $sc.Save()
    }
    finally {
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($shell)
    }

    if (-not (Test-Path -LiteralPath $linkPath)) {
        Write-Error "shortcut save reported success but '$linkPath' is not there."
        exit 1
    }

    Write-Status "wrote '$linkPath'  ->  '$target'"
    exit 0
}
catch {
    Write-Error "failed to write how-to-start shortcut: $($_.Exception.Message)"
    exit 1
}
