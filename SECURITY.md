# Security Policy

## Reporting a vulnerability

If you find a security issue in VoiceForge 2762, please report it privately instead of opening a public issue:

1. Email the maintainer with a description of the issue and steps to reproduce it.
2. Do not include credentials, private audio, tokens, or personal data in the report.
3. Allow reasonable time for a fix before any public disclosure.

## Scope

In scope:

- Authentication or access-control bypasses in the API
- Path traversal or arbitrary file access through API inputs
- Injection through text, filenames, or upload handling
- Exposure of secrets, tokens, or cloned voice data

Out of scope:

- The app being run without authentication on a public network (the default server is local-only by design — see README)
- Issues in third-party dependencies (report those upstream, or note them here so we can upgrade)

## Safe use

- Run the server on localhost unless you have added authentication, rate limiting, and restricted origins.
- Never commit Hugging Face tokens, voice recordings, cloned voice states, or generated audio to Git.
- Clone only voices you own or have permission to clone.
- Keep FFmpeg and Python dependencies up to date.
