from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from .config import get_settings
from .db import connect, initialize
from .ai import chat, ProviderError

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0")
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


@app.get("/")
def home():
    index = WEB_DIR / "index.html"
    if not index.exists():
        return {"message": "Your AI backend is running. Frontend is not installed yet."}
    return FileResponse(index)


@app.get("/api/health")
def health():
    return {"status": "ok", "app": settings.app_name, "version": "0.1.0"}


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


@app.post("/api/chat")
def send_chat(payload: ChatInput):
    try:
        answer, provider = chat([
            {"role": "system", "content": "You are Your AI, a helpful assistant. Be clear, safe, and honest about limitations."},
            {"role": "user", "content": payload.message.strip()},
        ])
        return {"reply": answer, "provider": provider}
    except ProviderError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
