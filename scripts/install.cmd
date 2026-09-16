@echo off
REM ============================================================================
REM North Forge Agent Installer (Portable Offline Edition)
REM ============================================================================
REM Runs the copy of install.ps1 that already lives next to this file.
REM Does not download https://hermes-agent.nousresearch.com/install.ps1

echo.
echo  North Forge Agent Installer
echo  Launching local PowerShell installer...
echo.

SET "LOCAL_INSTALLER=%~dp0install.ps1"

if not exist "%LOCAL_INSTALLER%" (
    echo.
    echo  Installation failed. Local installer not found:
    echo    %LOCAL_INSTALLER%
    echo  This USB checkout is incomplete. Re-run Deploy Console.
    echo  Manual run: powershell -ExecutionPolicy ByPass -File "%LOCAL_INSTALLER%"
    echo.
    pause
    exit /b 1
)

for %%I in ("%~dp0..") do set "AGENT_DIR=%%~fI"
for %%I in ("%~dp0..\..") do set "VOL=%%~fI"
for %%I in ("%AGENT_DIR%") do set "LEAF=%%~nxI"
set "HERMES_HOME=%VOL%\%LEAF%-data"

powershell -ExecutionPolicy ByPass -NoProfile -File "%LOCAL_INSTALLER%" -HermesHome "%HERMES_HOME%" -InstallDir "%AGENT_DIR%" -SkipComputerUse

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo  Installation failed. Please verify that '%LOCAL_INSTALLER%' exists on the drive.
    echo  Manual run: powershell -ExecutionPolicy ByPass -File "%LOCAL_INSTALLER%"
    echo.
    pause
    exit /b 1
)
