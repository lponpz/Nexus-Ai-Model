import sqlite3
from pathlib import Path
from .config import get_settings


def connect() -> sqlite3.Connection:
    settings = get_settings()
    db_path = Path(settings.database_path)
    if str(db_path) != ":memory:":
        db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(db_path))
    connection.row_factory = sqlite3.Row
    return connection


def initialize() -> None:
    with connect() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL DEFAULT 'General',
                description TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
                content TEXT NOT NULL,
                provider TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_message(role: str, content: str, provider: str = "") -> None:
    if role not in {"user", "assistant"}:
        raise ValueError("Unsupported message role")
    with connect() as db:
        db.execute(
            "INSERT INTO chat_messages (role, content, provider) VALUES (?, ?, ?)",
            (role, content, provider),
        )


def recent_messages(limit: int = 40) -> list[dict]:
    limit = max(1, min(int(limit), 100))
    with connect() as db:
        rows = db.execute(
            "SELECT id, role, content, provider, created_at "
            "FROM chat_messages ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(row) for row in reversed(rows)]
