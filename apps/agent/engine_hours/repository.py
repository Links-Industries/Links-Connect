from __future__ import annotations

from abc import ABC, abstractmethod

from .models import EngineHours


class EngineHoursRepository(ABC):
    @abstractmethod
    def get_by_machine_id(self, machine_id: int) -> EngineHours | None:
        raise NotImplementedError

    @abstractmethod
    def save(self, engine_hours: EngineHours) -> None:
        raise NotImplementedError
