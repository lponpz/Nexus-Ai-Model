from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from .config import get_settings
from .db import connect, initialize, recent_messages, save_message
from .ai import chat, ProviderError
from .plugin_builder import build_paper_plugin

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.3.0")
initialize()
ROOT = Path(__file__).resolve().parents[2]
WEB_DIR = ROOT / "frontend"
if WEB_DIR.exists():
    app.mount("/assets", StaticFiles(directory=WEB_DIR), name="assets")


class ProjectInput(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    category: str = Field(default="General", max_length=60)
    description: str = Field(default="", max_length=2000)


class ChatInput(BaseModel):
    message: str = Field(min_length=1, max_length=8000)


class PluginBuildInput(BaseModel):
    name: str = Field(min_length=1, max_length=60)
    package_name: str = Field(default="com.example.plugin", min_length=3, max_length=120)
    version: str = Field(default="1.0.0", max_length=20)
    minecraft_version: str = Field(default="1.21.4", max_length=20)


@app.get("/")
def home():
    index = WEB_DIR / "index.html"
    return FileResponse(index) if index.exists() else {"message": "Your AI backend is running."}


@app.get("/api/health")
def health():
    return {"status": "ok", "app": settings.app_name, "version": "0.3.0"}


@app.get("/api/projects")
def list_projects():
    with connect() as db:
        rows = db.execute(
            "SELECT id, name, category, description, created_at FROM projects ORDER BY id DESC"
        ).fetchall()
    return [dict(row) for row in rows]


@app.post("/api/projects")
def create_project(project: ProjectInput):
    with connect() as db:
        cursor = db.execute(
            "INSERT INTO projects (name, category, description) VALUES (?, ?, ?)",
            (project.name.strip(), project.category.strip(), project.description.strip()),
        )
        row = db.execute(
            "SELECT id, name, category, description, created_at FROM projects WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()
    return dict(row)


@app.get("/api/chat/history")
def get_chat_history():
    return recent_messages(100)


@app.post("/api/chat")
def send_chat(payload: ChatInput):
    message = payload.message.strip()
    history = recent_messages(20)
    messages = [
        {"role": "system", "content": "You are Your AI, a helpful assistant. Be clear, safe, and honest about limitations."}
    ]
    messages.extend({"role": item["role"], "content": item["content"]} for item in history)
    messages.append({"role": "user", "content": message})
    try:
        answer, provider = chat(messages)
    except ProviderError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    save_message("user", message)
    save_message("assistant", answer, provider)
    return {"reply": answer, "provider": provider}


@app.post("/api/minecraft/paper-plugin.zip")
def generate_paper_plugin(payload: PluginBuildInput):
    try:
        archive = build_paper_plugin(
            payload.name, payload.package_name, payload.version, payload.minecraft_version
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    filename = "".join(ch for ch in payload.name if ch.isalnum() or ch in "-_") or "PaperPlugin"
    return Response(
        content=archive,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{filename}.zip"'},
    )
