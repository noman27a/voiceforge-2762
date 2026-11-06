#!/bin/bash
# VoiceForge 2762 — one-command start (Linux/Mac). Creates venv on first run.
set -e
cd "$(dirname "$0")"
if [ ! -d .venv ]; then
  python3 -m venv .venv
  TMPDIR="$PWD/.tmp" .venv/bin/pip install --quiet --disable-pip-version-check -r requirements.txt
fi
exec .venv/bin/python run.py
