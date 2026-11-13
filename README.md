# Your AI

A local-first, hybrid AI assistant project for Windows and Android-friendly browsers.

## Current status

This repository is an **early working foundation**, not the complete feature set yet. Verified foundation components currently include:
- FastAPI backend with a local SQLite project store and persistent chat history
- Chat endpoint that selects an OpenAI-compatible cloud provider when configured, otherwise attempts a local Ollama model
- Recent conversation context supplied to the chat provider
- Responsive browser dashboard for chat and project creation
- Health/status endpoint
- Paper plugin **source-project ZIP generator** (creates Maven/Java/plugin.yml files; it does not compile a JAR)
- GitHub Actions workflow; the latest observed workflow run completed successfully, including dependency installation and the unit-test step

The larger roadmap (Minecraft Creator Studio, Coding & App Builder, Video & Animation, 3D, voice, image understanding/generation, GitHub/VS Code integrations, agent workflows and security center) remains planned and will be delivered in separately verified milestones. A feature is not considered complete until its implementation, tests, documented configuration and verified run/build exist.

## Requirements
- Python 3.10+
- Optional: an OpenAI-compatible API key and endpoint, or Ollama installed locally
- Internet is not required for the UI and local project/chat storage; offline chat requires a local model such as Ollama to be installed and running.

## Run on Windows
1. Install Python 3.10 or newer.
2. Open a terminal in this repository.
3. Create a virtual environment: `python -m venv .venv`
4. Activate it:
   - PowerShell: `.venv\\Scripts\\Activate.ps1`
   - CMD: `.venv\\Scripts\\activate.bat`
5. Install dependencies: `pip install -r requirements.txt`
6. Copy `.env.example` to `.env` and edit only the settings you need.
7. Start: `uvicorn backend.app.main:app --host 127.0.0.1 --port 8000`
8. Open http://127.0.0.1:8000

## AI provider configuration
Cloud (OpenAI-compatible): set `AI_BASE_URL`, `AI_API_KEY`, and `AI_MODEL`.
Local Ollama: set `OLLAMA_BASE_URL` and `OLLAMA_MODEL` to a model already installed in Ollama. If no cloud key is configured, the backend attempts the local Ollama endpoint. This is a provider fallback, not yet the planned lightweight/advanced local-model selector.

Chat history is stored in the local SQLite database. There is currently no cloud conversation sync; future sync must remain off until the user explicitly gives permission.

Never commit API keys, access tokens, passwords, or private data. Keep them in your local `.env` file.

## Safety and permissions
The starter server binds to localhost by default. It does not run shell commands, install software, edit arbitrary project files, control the desktop, or modify Minecraft servers. Full AI Developer Mode is not implemented yet. Future file changes, terminal commands, builds, GitHub writes and system actions must require explicit user approval, reject dangerous commands, keep an audit trail and create backups before major changes.

## Development roadmap
See `docs/ROADMAP.md`. Current completed foundation work is deliberately limited; the remaining approved feature set is planned, not represented by the dashboard as already working.
