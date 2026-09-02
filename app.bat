@echo off
REM Launcher script for DigiShell on Windows
python -m digishell.cli %*
if %ERRORLEVEL% NEQ 0 (
    echo DigiShell exited with code %ERRORLEVEL%
)
