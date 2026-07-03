from __future__ import annotations

import sqlite3

from ..infrastructure import Database
from .models import EngineSession
from .repository import EngineHoursRepository


INSERT_ENGINE_SESSION_SQL = """
INSERT INTO engine_sessions (started_at, stopped_at, duration_seconds)
VALUES (?, ?, ?)
"""

SELECT_ENGINE_SESSIONS_SQL = """
SELECT started_at, stopped_at, duration_seconds
FROM engine_sessions
ORDER BY started_at ASC, id ASC
"""


class SQLiteEngineHoursRepository(EngineHoursRepository):
    def __init__(self, database: Database) -> None:
        self._database = database

    def save_session(self, session: EngineSession) -> None:
        with self._database.connect() as connection:
            connection.execute(
                INSERT_ENGINE_SESSION_SQL,
                (
                    session.started_at,
                    session.stopped_at,
                    session.duration_seconds,
                ),
            )

    def load_sessions(self) -> list[EngineSession]:
        with self._database.connect() as connection:
            rows = connection.execute(SELECT_ENGINE_SESSIONS_SQL).fetchall()

        return [self._map_session(row) for row in rows]

    @staticmethod
    def _map_session(row: sqlite3.Row) -> EngineSession:
        return EngineSession(
            started_at=float(row["started_at"]),
            stopped_at=float(row["stopped_at"]),
            duration_seconds=float(row["duration_seconds"]),
        )
