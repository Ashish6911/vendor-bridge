@echo off
SETLOCAL
set PYTHONPATH=%~dp0
py -m uvicorn vendorbridge.main:app --reload --host 127.0.0.1 --port 8000
ENDLOCAL