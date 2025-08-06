@echo off
echo Iniciando Aurora-Core Server...
set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
poetry run uvicorn src.aurora_platform.main:app --reload --host 0.0.0.0 --port 8000
