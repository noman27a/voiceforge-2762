# VoiceForge 2762 — AI Voiceover Studio

Local-first text-to-speech studio powered by **Pocket TTS** (Kyutai).
Generate unlimited voiceovers from text, use 26 built-in voices, clone
voices from a reference recording, mix background music, and batch-generate
whole scripts — all from a browser UI. No API credits, no per-minute charges.

Built from scratch for the **2762 AI** project. Inspired by the feature set
of the VoiceForge repo — this is an original implementation, not a copy of
its source (that repo ships no license, so its code is not reused here).

## Features

- **Studio:** text → speech with speed, pitch, reverb, WAV/MP3 output
- **26 built-in voices** (female + male), with previews
- **Voice cloning:** upload a 10–30s reference recording → new voice profile
- **Batch generation:** many lines → one ZIP of audio files
- **Background music:** upload BGM, auto-ducked under the voice
- **History:** recent generations with playback + download-all ZIP
- **Setup page:** model status + Hugging Face token for cloning access

## Quick start (Windows / Linux / Mac)

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Open http://127.0.0.1:7860

First model load downloads the Pocket TTS weights (a few hundred MB) —
be patient the first time. FFmpeg must be installed for pitch/reverb/BGM
and MP3 output.

## Voice cloning setup

Pocket TTS's cloning model is gated on Hugging Face:

1. Create a free account at https://huggingface.co
2. Open the Pocket TTS model page and accept its license
3. Create a token at https://huggingface.co/settings/tokens (`hf_…`)
4. Paste it in the app's **Setup** tab → Save Token

Cloning works only with your own voice or a recording you have
permission to clone.

## Project structure

```
voiceforge2762/
├── run.py                 # entry point — starts the server
├── requirements.txt
├── engine/
│   ├── server.py          # FastAPI app + API routes
│   ├── tts_engine.py      # Pocket TTS wrapper
│   └── voice_registry.py  # built-in + cloned voice metadata
├── static/                # web UI (index.html, css, js)
└── data/                  # generated audio, clones, BGM, model cache
```

## Notes

- Local use by default. Do not expose publicly without auth + rate limits.
- Generated audio and cloned voice states stay on your machine.
- "Unlimited" means no API quota — generation is limited only by your
  own hardware.
