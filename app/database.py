# Database location

import os
import sqlite3
from pathlib import Path
from datetime import datetime

APP_NAME = "PrepaTyping"

# Persistent application data directory on Linux
DATA_HOME = Path(
    os.environ.get(
        "XDG_DATA_HOME",
        str(Path.home() / ".local" / "share")
    )
).expanduser()

DATA_DIR = DATA_HOME / APP_NAME
DATABASE_PATH = DATA_DIR / "prepatyping.db"
DATABASE_VERSION = 1



def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    with get_connection() as connection:

        current_version = connection.execute(
            "PRAGMA user_version"
        ).fetchone()[0]

        if current_version > DATABASE_VERSION:
            raise RuntimeError(
                "Database version is newer than "
                "this application supports."
            )

        if current_version < 1:
            # Initial database schema
            connection.execute("""
                CREATE TABLE IF NOT EXISTS practice_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    level TEXT NOT NULL,
                    exercises_completed INTEGER NOT NULL,
                    average_wpm REAL NOT NULL,
                    average_accuracy REAL NOT NULL,
                    total_seconds REAL NOT NULL,
                    completed_at TEXT NOT NULL
                )
            """)

            # Verify existing schema before marking version 1
            required_columns = {
                "id",
                "level",
                "exercises_completed",
                "average_wpm",
                "average_accuracy",
                "total_seconds",
                "completed_at",
            }

            existing_columns = {
                row["name"]
                for row in connection.execute(
                    "PRAGMA table_info(practice_sessions)"
                )
            }

            if not required_columns.issubset(existing_columns):
                raise RuntimeError(
                    "Database schema is missing required columns."
                )

            connection.execute(
                "PRAGMA user_version = 1"
            )


def save_session(
    level,
    exercises_completed,
    average_wpm,
    average_accuracy,
    total_seconds,
):
    completed_at = datetime.now().astimezone().isoformat(
        timespec="seconds"
    )

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO practice_sessions (
                level,
                exercises_completed,
                average_wpm,
                average_accuracy,
                total_seconds,
                completed_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                level,
                exercises_completed,
                average_wpm,
                average_accuracy,
                total_seconds,
                completed_at,
            ),
        )

        return cursor.lastrowid


def get_practice_history():
    with get_connection() as connection:
        connection.row_factory = sqlite3.Row

        cursor = connection.execute("""
            SELECT
                id,
                level,
                exercises_completed,
                average_wpm,
                average_accuracy,
                total_seconds,
                completed_at
            FROM practice_sessions
            ORDER BY completed_at DESC, id DESC
        """)

        return [dict(row) for row in cursor.fetchall()]
