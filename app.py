"""Hugging Face Spaces entry point (Gradio SDK, free tier).

The Space runs `python app.py`. This launches the FastAPI VoiceForge
server with uvicorn on the port HF assigns (default 7860) — no Gradio
UI is needed; the static frontend in static/ is served by FastAPI.
"""
import os
import sys
import threading
import time
from pathlib import Path

import spaces

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / "engine"))


@spaces.GPU(duration=30)
def _zerogpu_startup_check():
    """Dummy GPU function (never called).

    ZeroGPU Spaces refuse to start without at least one @spaces.GPU
    function. VoiceForge runs Pocket TTS on the Space's CPU, so this
    function is never called and uses no GPU quota — it only exists
    so there is something for the startup report (sent by
    _report_zerogpu_functions below) to announce.
    """
    return None


def _report_zerogpu_functions():
    """Report the @spaces.GPU functions to the ZeroGPU backend.

    The spaces library only sends this report when a Gradio app
    launches (it hooks Blocks.launch), and VoiceForge is a FastAPI
    app, so the report would never fire and the Space fails startup
    with "No @spaces.GPU function detected". Call the library's own
    startup routine directly, in a background thread with retries so
    a slow device API cannot block the server. Off ZeroGPU (local
    dev) the routine does not exist and this is a no-op.
    """
    try:
        from spaces.zero import startup as _zerogpu_startup
    except Exception:
        return
    for _ in range(18):  # ~90s of retries
        try:
            _zerogpu_startup()
            return
        except Exception:
            time.sleep(5)


threading.Thread(target=_report_zerogpu_functions, daemon=True).start()

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
