$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = (Get-Command python -ErrorAction Stop).Source
$logFile = Join-Path $projectRoot "data\launcher.log"

# Python 3.14 on this Windows installation cannot create a virtual environment.
# Use its user-level package location instead so the desktop shortcut remains usable.
& $python -m pip install -q --user -r (Join-Path $projectRoot "requirements.txt") 2>> $logFile
Set-Location $projectRoot
& $python -m streamlit run app\main.py --server.headless true 2>> $logFile
