"""Hugging Face Spaces entry point (Gradio SDK, free tier).

The Space runs `python app.py`. This launches the FastAPI VoiceForge
server with uvicorn on the port HF assigns (default 7860) — no Gradio
UI is needed; the static frontend in static/ is served by FastAPI.
"""
import os
import sys
from pathlib import Path

import spaces

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / "engine"))


@spaces.GPU(duration=30)
def _zerogpu_startup_check():
    """Dummy GPU function (never called).

    ZeroGPU Spaces refuse to start unless a @spaces.GPU function is
    visible in the entry file (app.py) — a decorator in an imported
    module is not detected. VoiceForge runs Pocket TTS on the Space's
    CPU, so this function is never called and uses no GPU quota; it
    only satisfies the startup check.
    """
    return None

# Keep HF model cache inside the project so installs stay portable.
os.environ.setdefault("HF_HOME", str(BASE_DIR / "data" / "hf_cache"))

if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", "7860"))
    print("VoiceForge 2762 — AI Voiceover Studio (Hugging Face Space)")
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=port,
        log_level="warning",
        access_log=False,
    )
