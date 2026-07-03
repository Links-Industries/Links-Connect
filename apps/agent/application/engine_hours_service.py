from __future__ import annotations

from apps.agent.engine_hours.models import EngineSession
from apps.agent.engine_hours.repository import EngineHoursRepository

SECONDS_PER_HOUR = 3600.0


class EngineHoursService:
    def __init__(self, repository: EngineHoursRepository) -> None:
        self._repository = repository

    def load_sessions(self) -> list[EngineSession]:
        return self._repository.load_sessions()

    def total_sessions(self) -> int:
        return len(self.load_sessions())

    def total_engine_hours(self) -> float:
        return sum(
            session.duration_seconds for session in self.load_sessions()
        ) / SECONDS_PER_HOUR

    def last_session_duration(self) -> float:
        sessions = self.load_sessions()

        if not sessions:
            return 0.0

        return sessions[-1].duration_seconds
