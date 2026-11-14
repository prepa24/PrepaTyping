
import sqlite3
from pathlib import Path
from datetime import datetime

# Database location
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "prepatyping.db"


def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    with get_connection() as connection:
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
