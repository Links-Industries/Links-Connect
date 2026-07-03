from __future__ import annotations

import time

from .exceptions import EngineAlreadyRunningError, EngineNotRunningError
from .models import EngineSession


class EngineHoursCounter:
    def __init__(self) -> None:
        self._started_at: float | None = None

    def start(self) -> None:
        if self.is_running():
            raise EngineAlreadyRunningError("Engine session is already running.")

        self._started_at = time.monotonic()

    def stop(self) -> EngineSession:
        if self._started_at is None:
            raise EngineNotRunningError("Engine session is not running.")

        stopped_at = time.monotonic()
        started_at = self._started_at
        self._started_at = None

        return EngineSession(
            started_at=started_at,
            stopped_at=stopped_at,
            duration_seconds=stopped_at - started_at,
        )

    def is_running(self) -> bool:
        return self._started_at is not None
