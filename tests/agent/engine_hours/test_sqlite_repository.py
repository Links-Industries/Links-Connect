from __future__ import annotations

from pathlib import Path

import pytest

from apps.agent.engine_hours.models import EngineSession
from apps.agent.engine_hours.sqlite_repository import SQLiteEngineHoursRepository
from apps.agent.infrastructure import Database


@pytest.fixture
def repository(tmp_path: Path) -> SQLiteEngineHoursRepository:
    database = Database(tmp_path / "links_connect_test.db")
    database.initialize_schema()
    return SQLiteEngineHoursRepository(database)


def test_save_session_stores_completed_engine_session(
    repository: SQLiteEngineHoursRepository,
) -> None:
    session = EngineSession(
        started_at=100.0,
        stopped_at=145.25,
        duration_seconds=45.25,
    )

    repository.save_session(session)

    assert repository.load_sessions() == [session]


def test_load_sessions_returns_empty_list_when_no_sessions_exist(
    repository: SQLiteEngineHoursRepository,
) -> None:
    assert repository.load_sessions() == []


def test_load_sessions_returns_all_stored_engine_sessions(
    repository: SQLiteEngineHoursRepository,
) -> None:
    first_session = EngineSession(
        started_at=100.0,
        stopped_at=110.0,
        duration_seconds=10.0,
    )
    second_session = EngineSession(
        started_at=200.0,
        stopped_at=230.5,
        duration_seconds=30.5,
    )

    repository.save_session(first_session)
    repository.save_session(second_session)

    assert repository.load_sessions() == [first_session, second_session]


def test_load_sessions_orders_sessions_by_start_time(
    repository: SQLiteEngineHoursRepository,
) -> None:
    later_session = EngineSession(
        started_at=300.0,
        stopped_at=320.0,
        duration_seconds=20.0,
    )
    earlier_session = EngineSession(
        started_at=100.0,
        stopped_at=150.0,
        duration_seconds=50.0,
    )

    repository.save_session(later_session)
    repository.save_session(earlier_session)

    assert repository.load_sessions() == [earlier_session, later_session]
