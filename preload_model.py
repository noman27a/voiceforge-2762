#!/usr/bin/env python3
"""Preload the Pocket TTS model weights into the local cache.

Run once after installing requirements so the first server start is fast:

    python preload_model.py

The model is cached under data/hf_cache (or your HF_HOME).
"""
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
os.environ.setdefault("HF_HOME", str(BASE_DIR / "data" / "hf_cache"))
sys.path.insert(0, str(BASE_DIR / "engine"))

import asyncio
from tts_engine import TTSEngine


async def main():
    engine = TTSEngine()
    print("Loading Pocket TTS model (first run downloads weights)…")
    await engine.load_model()
    status = engine.get_status()
    if status["model_loaded"]:
        print("Model ready. Voice cloning available:", status["voice_cloning"])
        if not status["voice_cloning"]:
            print("Tip: set an HF_TOKEN with Pocket TTS access to enable cloning.")
    else:
        print("Model failed to load:", status["setup_status"])
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
