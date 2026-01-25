@echo off
setlocal enabledelayedexpansion

echo Uruchamianie testów pytest...
pytest tests/ -v --cov=app --cov-report=term-missing
if %errorlevel% neq 0 (
    echo Pytest nieudany!
    exit /b 1
)

echo Uruchamianie pylint...
pylint --ignore=.venv --disable=C0114,C0115,C0116,R0903 .
if %errorlevel% neq 0 (
    echo Pylint nieudany!
    exit /b 2
)

echo Wszystko OK!
