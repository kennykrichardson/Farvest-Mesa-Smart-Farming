Set-Location "$PSScriptRoot\backend"
if (-not (Test-Path ".venv")) { py -3.12 -m venv .venv }
& ".\.venv\Scripts\Activate.ps1"
python -m pip install -r requirements.txt
uvicorn api:app --reload --host 127.0.0.1 --port 8000
