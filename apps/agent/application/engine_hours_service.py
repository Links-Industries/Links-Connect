from __future__ import annotations

from apps.agent.engine_hours.models import EngineSession
from apps.agent.engine_hours.repository import EngineHoursRepository


class EngineHoursService:
    def __init__(self, repository: EngineHoursRepository) -> None:
        self._repository = repository

    def load_sessions(self) -> list[EngineSession]:
        return self._repository.load_sessions()

    def total_sessions(self) -> int:
        return len(self.load_sessions())
