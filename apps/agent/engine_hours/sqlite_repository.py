from __future__ import annotations

import sqlite3
from datetime import datetime

from ..infrastructure import Database
from .models import EngineHours
from .repository import EngineHoursRepository


class SQLiteEngineHoursRepository(EngineHoursRepository):
    def __init__(self, database: Database) -> None:
        self._database = database

    def get_by_machine_id(self, machine_id: int) -> EngineHours | None:
        with self._database.connect() as connection:
            row = connection.execute(
                """
                SELECT id, machine_id, total_seconds, updated_at
                FROM engine_hours
                WHERE machine_id = ?
                ORDER BY updated_at DESC
                LIMIT 1
                """,
                (machine_id,),
            ).fetchone()

        if row is None:
            return None

        return self._map_row(row)

    def save(self, engine_hours: EngineHours) -> None:
        if engine_hours.id is None:
            self._insert(engine_hours)
            return

        self._upsert(engine_hours)

    def _insert(self, engine_hours: EngineHours) -> None:
        with self._database.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO engine_hours (machine_id, total_seconds, updated_at)
                VALUES (?, ?, ?)
                """,
                (
                    engine_hours.machine_id,
                    engine_hours.total_seconds,
                    engine_hours.updated_at.isoformat(),
                ),
            )
            engine_hours.id = int(cursor.lastrowid)

    def _upsert(self, engine_hours: EngineHours) -> None:
        with self._database.connect() as connection:
            connection.execute(
                """
                INSERT INTO engine_hours (id, machine_id, total_seconds, updated_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    machine_id = excluded.machine_id,
                    total_seconds = excluded.total_seconds,
                    updated_at = excluded.updated_at
                """,
                (
                    engine_hours.id,
                    engine_hours.machine_id,
                    engine_hours.total_seconds,
                    engine_hours.updated_at.isoformat(),
                ),
            )

    @staticmethod
    def _map_row(row: sqlite3.Row) -> EngineHours:
        return EngineHours(
            id=int(row["id"]),
            machine_id=int(row["machine_id"]),
            total_seconds=int(row["total_seconds"]),
            updated_at=datetime.fromisoformat(str(row["updated_at"])),
        )
