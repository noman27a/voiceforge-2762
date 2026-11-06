# Contributing to VoiceForge 2762

Thanks for your interest in improving VoiceForge 2762. Issues and pull requests are welcome.

## Reporting a bug

Open an issue with:

- Your operating system and Python version
- The exact steps to reproduce the problem
- What you expected vs. what happened
- Sanitized logs (remove tokens, file paths with personal names, and audio)

Never include credentials, private audio, or personal data in an issue.

## Suggesting a feature

Open an issue describing the use case first — what voiceover task it helps with and how it should behave. Small, focused proposals are easier to review than large redesigns.

## Pull requests

1. Fork the repository and create a branch from `main`.
2. Keep changes focused: one feature or fix per pull request.
3. Run the checks before submitting:
   ```bash
   pip install -r requirements-dev.txt
   python -m pytest tests/
   python -m compileall engine/
   ```
4. Update the README or docs when a change affects setup, API routes, or the UI.
5. Do not commit generated audio, cloned voice states, tokens, logs, or virtual environments.

## Code style

- Python: readable, typed where it helps, no unused imports.
- JavaScript: plain, dependency-free frontend code.
- Keep the local-first design: no paid APIs, no tracking, no remote calls except model downloads.
