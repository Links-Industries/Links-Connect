from __future__ import annotations

from abc import ABC, abstractmethod

from .models import EngineSession


class EngineHoursRepository(ABC):
    @abstractmethod
    def save_session(self, session: EngineSession) -> None:
        raise NotImplementedError

    @abstractmethod
    def load_sessions(self) -> list[EngineSession]:
        raise NotImplementedError
