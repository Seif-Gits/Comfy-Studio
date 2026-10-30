#!/bin/sh
# Linux / macOS launcher: starts ComfyUI (terminal only) and opens Comfy Studio in the browser.
cd "$(dirname "$0")"
for p in ../venv/bin/python ../.venv/bin/python; do [ -x "$p" ] && PY="$p" && break; done
exec "${PY:-python3}" studio.py
