# Your AI

A local-first, hybrid AI assistant project for Windows and Android-friendly browsers.

## Current status

This repository starts with a **working starter foundation**, not the complete feature set yet. The first milestone provides:
- FastAPI backend with a local SQLite project store
- Chat endpoint with an OpenAI-compatible cloud provider or local Ollama fallback
- Small responsive web interface
- Health/status endpoint
- Localhost-only default binding and environment-based secrets

The larger roadmap (Minecraft Creator Studio, Coding & App Builder, Video & Animation, 3D, voice, GitHub/VS Code integrations, agent workflows and security center) will be delivered in separately tested milestones. A feature is not considered complete until its implementation and tests exist.

## Requirements
- Python 3.10+
- Optional: an OpenAI-compatible API key and endpoint, or Ollama installed locally
- Internet is not required for the UI and project storage; offline chat requires a local model such as Ollama to be installed and running.

## Run on Windows
1. Install Python 3.10 or newer.
2. Open a terminal in this repository.
3. Create a virtual environment: `python -m venv .venv`
4. Activate it:
   - PowerShell: `.venv\Scripts\Activate.ps1`
   - CMD: `.venv\Scripts\activate.bat`
5. Install dependencies: `pip install -r requirements.txt`
6. Copy `.env.example` to `.env` and edit only the settings you need.
7. Start: `uvicorn backend.app.main:app --host 127.0.0.1 --port 8000`
8. Open http://127.0.0.1:8000

## AI provider configuration
Cloud (OpenAI-compatible): set `AI_BASE_URL`, `AI_API_KEY`, and `AI_MODEL`.
Local Ollama: set `OLLAMA_BASE_URL` and `OLLAMA_MODEL` to a model already installed in Ollama. If no cloud key is configured, the backend attempts the local Ollama endpoint.

Never commit API keys, access tokens, passwords, or private data. Keep them in your local `.env` file.

## Safety and permissions
The starter server binds to localhost by default. It does not run shell commands, install software, edit arbitrary files, control the desktop, or modify Minecraft servers. Future agent and integration features must use explicit per-action approval, least-privilege credentials, audit logs and a stop control.

## Development roadmap
See `docs/ROADMAP.md`. The next milestones cover persistent chat history, Minecraft Creator Studio, Coding Studio, creative studios, offline knowledge and an approval-based agent/security center.
