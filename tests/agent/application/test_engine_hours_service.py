from __future__ import annotations

from apps.agent.application import EngineHoursService
from apps.agent.engine_hours.models import EngineSession
from apps.agent.engine_hours.repository import EngineHoursRepository


class InMemoryEngineHoursRepository(EngineHoursRepository):
    def __init__(self, sessions: list[EngineSession]) -> None:
        self._sessions = sessions

    def save_session(self, session: EngineSession) -> None:
        self._sessions.append(session)

    def load_sessions(self) -> list[EngineSession]:
        return list(self._sessions)


def test_load_sessions_delegates_to_repository() -> None:
    session = EngineSession(started_at=10.0, stopped_at=15.0, duration_seconds=5.0)
    service = EngineHoursService(InMemoryEngineHoursRepository([session]))

    assert service.load_sessions() == [session]


def test_total_sessions_counts_loaded_sessions() -> None:
    sessions = [
        EngineSession(started_at=10.0, stopped_at=15.0, duration_seconds=5.0),
        EngineSession(started_at=20.0, stopped_at=25.0, duration_seconds=5.0),
    ]
    service = EngineHoursService(InMemoryEngineHoursRepository(sessions))

    assert service.total_sessions() == 2


def test_total_engine_hours_sums_session_durations_in_hours() -> None:
    sessions = [
        EngineSession(started_at=10.0, stopped_at=3610.0, duration_seconds=3600.0),
        EngineSession(started_at=4000.0, stopped_at=5800.0, duration_seconds=1800.0),
    ]
    service = EngineHoursService(InMemoryEngineHoursRepository(sessions))

    assert service.total_engine_hours() == 1.5


def test_last_session_duration_returns_last_completed_session_duration() -> None:
    sessions = [
        EngineSession(started_at=10.0, stopped_at=3610.0, duration_seconds=3600.0),
        EngineSession(started_at=4000.0, stopped_at=5800.0, duration_seconds=1800.0),
    ]
    service = EngineHoursService(InMemoryEngineHoursRepository(sessions))

    assert service.last_session_duration() == 1800.0


def test_last_session_duration_returns_zero_when_no_sessions_exist() -> None:
    service = EngineHoursService(InMemoryEngineHoursRepository([]))

    assert service.last_session_duration() == 0.0
