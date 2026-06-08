"""
htmforge-demo — db.py
SQLite-Datenbank. Setup, Seed-Daten, CRUD-Queries.
"""

import sqlite3
import os
from datetime import datetime, timedelta
import random

DB_PATH = os.path.join(os.path.dirname(__file__), "demo.db")


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Erstellt Tabellen und füllt mit Seed-Daten wenn leer."""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT    NOT NULL,
                email       TEXT    NOT NULL UNIQUE,
                role        TEXT    NOT NULL DEFAULT 'viewer',
                status      TEXT    NOT NULL DEFAULT 'active',
                created_at  TEXT    NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS api_keys (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL REFERENCES users(id),
                key_preview TEXT    NOT NULL,
                created_at  TEXT    NOT NULL
            )
        """)
        conn.commit()

        # Seed nur wenn leer
        if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
            _seed(conn)


def _seed(conn: sqlite3.Connection):
    seed_users = [
        ("Ada Lovelace",    "ada@example.com",    "admin",   "active"),
        ("Grace Hopper",    "grace@example.com",  "editor",  "active"),
        ("Alan Turing",     "turing@example.com", "editor",  "active"),
        ("Linus Torvalds",  "linus@example.com",  "viewer",  "active"),
        ("Guido van Rossum","guido@example.com",  "viewer",  "active"),
        ("Dennis Ritchie",  "dennis@example.com", "viewer",  "inactive"),
        ("Ken Thompson",    "ken@example.com",    "editor",  "inactive"),
    ]
    base = datetime.now()
    for i, (name, email, role, status) in enumerate(seed_users):
        created = (base - timedelta(days=random.randint(10, 300))).strftime("%Y-%m-%d %H:%M:%S")
        conn.execute(
            "INSERT INTO users (name, email, role, status, created_at) VALUES (?, ?, ?, ?, ?)",
            (name, email, role, status, created),
        )
        uid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.execute(
            "INSERT INTO api_keys (user_id, key_preview, created_at) VALUES (?, ?, ?)",
            (uid, f"nd_{uid:04d}...{i:04x}", created),
        )
    conn.commit()


# ── Queries ───────────────────────────────────────────────

def get_users(search: str = "") -> list[sqlite3.Row]:
    with get_db() as conn:
        if search:
            q = f"%{search}%"
            return conn.execute(
                "SELECT * FROM users WHERE name LIKE ? OR email LIKE ? ORDER BY created_at DESC",
                (q, q),
            ).fetchall()
        return conn.execute("SELECT * FROM users ORDER BY created_at DESC").fetchall()


def get_user(user_id: int) -> sqlite3.Row | None:
    with get_db() as conn:
        return conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


def create_user(name: str, email: str, role: str, status: str) -> int:
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_db() as conn:
        conn.execute(
            "INSERT INTO users (name, email, role, status, created_at) VALUES (?, ?, ?, ?, ?)",
            (name, email, role, status, created_at),
        )
        conn.commit()
        return conn.execute("SELECT last_insert_rowid()").fetchone()[0]


def update_user(user_id: int, name: str, email: str, role: str, status: str):
    with get_db() as conn:
        conn.execute(
            "UPDATE users SET name=?, email=?, role=?, status=? WHERE id=?",
            (name, email, role, status, user_id),
        )
        conn.commit()


def delete_user(user_id: int):
    with get_db() as conn:
        conn.execute("DELETE FROM api_keys WHERE user_id=?", (user_id,))
        conn.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()


def get_stats() -> dict:
    with get_db() as conn:
        total   = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        active  = conn.execute("SELECT COUNT(*) FROM users WHERE status='active'").fetchone()[0]
        admins  = conn.execute("SELECT COUNT(*) FROM users WHERE role='admin'").fetchone()[0]
        api_keys = conn.execute("SELECT COUNT(*) FROM api_keys").fetchone()[0]
        return {
            "total_users": total,
            "active_users": active,
            "inactive_users": total - active,
            "admins": admins,
            "api_keys": api_keys,
        }