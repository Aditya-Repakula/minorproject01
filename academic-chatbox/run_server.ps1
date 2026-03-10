Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$venv = Join-Path $PSScriptRoot ".venv"
if (!(Test-Path $venv)) {
  python -m venv ".venv"
}

. ".venv\\Scripts\\Activate.ps1"

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

python app.py
