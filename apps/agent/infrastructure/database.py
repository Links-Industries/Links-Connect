from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path


MACHINE_COLUMN_DEFINITIONS: dict[str, str] = {
    "manufacturer": "TEXT NOT NULL DEFAULT ''",
    "model": "TEXT NOT NULL DEFAULT ''",
    "year": "INTEGER NOT NULL DEFAULT 0",
    "location": "TEXT NOT NULL DEFAULT ''",
    "updated_at": "TEXT NOT NULL DEFAULT ''",
}

SCHEMA_STATEMENTS: tuple[str, ...] = (
    """
    CREATE TABLE IF NOT EXISTS machines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        manufacturer TEXT NOT NULL,
        model TEXT NOT NULL,
        serial_number TEXT NOT NULL UNIQUE,
        year INTEGER NOT NULL,
        location TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS engine_hours (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        machine_id INTEGER NOT NULL,
        total_seconds INTEGER NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (machine_id) REFERENCES machines (id) ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS engine_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        started_at REAL NOT NULL,
        stopped_at REAL NOT NULL,
        duration_seconds REAL NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS gps_positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        machine_id INTEGER NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        speed REAL NOT NULL,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (machine_id) REFERENCES machines (id) ON DELETE CASCADE
    )
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_machines_serial_number
    ON machines (serial_number)
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_engine_hours_machine_id
    ON engine_hours (machine_id)
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_engine_sessions_started_at
    ON engine_sessions (started_at)
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_gps_positions_machine_id_timestamp
    ON gps_positions (machine_id, timestamp)
    """,
)


class Database:
    def __init__(self, database_path: Path) -> None:
        self._database_path = database_path

    @property
    def database_path(self) -> Path:
        return self._database_path

    def initialize_schema(self) -> None:
        self._database_path.parent.mkdir(parents=True, exist_ok=True)

        with self.connect() as connection:
            connection.executescript(";\n".join(SCHEMA_STATEMENTS))
            self._ensure_machine_columns(connection)

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self._database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")

        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    @staticmethod
    def _ensure_machine_columns(connection: sqlite3.Connection) -> None:
        existing_columns = {
            str(row["name"])
            for row in connection.execute("PRAGMA table_info(machines)").fetchall()
        }

        for column_name, column_definition in MACHINE_COLUMN_DEFINITIONS.items():
            if column_name not in existing_columns:
                connection.execute(
                    f"ALTER TABLE machines ADD COLUMN {column_name} {column_definition}"
                )
