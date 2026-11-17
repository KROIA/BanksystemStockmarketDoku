@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\mkdocs.exe" (
  echo Creating the Python environment, this takes a minute...
  python -m venv .venv
  ".venv\Scripts\python.exe" -m pip install -r requirements.txt
)
echo Open http://127.0.0.1:8000 in your browser. Close this window to stop the preview.
".venv\Scripts\mkdocs.exe" serve -a 127.0.0.1:8000
pause
