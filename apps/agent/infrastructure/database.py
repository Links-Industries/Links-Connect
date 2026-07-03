from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path


SCHEMA_STATEMENTS: tuple[str, ...] = (
    """
    CREATE TABLE IF NOT EXISTS machines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        serial_number TEXT NOT NULL UNIQUE,
        created_at TEXT NOT NULL
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
    CREATE INDEX IF NOT EXISTS idx_engine_hours_machine_id
    ON engine_hours (machine_id)
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
