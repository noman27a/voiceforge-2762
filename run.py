#!/usr/bin/env python3
"""VoiceForge 2762 — start the local voiceover studio server."""
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / "engine"))

# Keep HF model cache inside the project so installs stay portable.
os.environ.setdefault("HF_HOME", str(BASE_DIR / "data" / "hf_cache"))

if __name__ == "__main__":
    import uvicorn

    print("VoiceForge 2762 — AI Voiceover Studio")
    print("Open: http://127.0.0.1:7860")
    uvicorn.run(
        "server:app",
        host="127.0.0.1",
        port=7860,
        log_level="warning",
        access_log=False,
    )
