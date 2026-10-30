@echo off
title Comfy Studio
cd /d "%~dp0"
rem Use ComfyUI's own Python: portable build first, then a venv next to main.py, then system Python.
set "PY="
if exist "..\..\python_embeded\python.exe" set "PY=..\..\python_embeded\python.exe"
if not defined PY if exist "..\venv\Scripts\python.exe" set "PY=..\venv\Scripts\python.exe"
if not defined PY if exist "..\.venv\Scripts\python.exe" set "PY=..\.venv\Scripts\python.exe"
if not defined PY set "PY=python"
"%PY%" -s studio.py
echo.
echo Comfy Studio has stopped. You can close this window.
pause
