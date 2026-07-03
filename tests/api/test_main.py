from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from apps.agent.application import EngineHoursService
from apps.agent.engine_hours.models import EngineSession
from apps.agent.engine_hours.repository import EngineHoursRepository
from apps.api.dependencies import get_engine_hours_service
from apps.api.main import app


class InMemoryEngineHoursRepository(EngineHoursRepository):
    def __init__(self, sessions: list[EngineSession] | None = None) -> None:
        self._sessions = sessions if sessions is not None else []

    def save_session(self, session: EngineSession) -> None:
        self._sessions.append(session)

    def load_sessions(self) -> list[EngineSession]:
        return list(self._sessions)


@pytest.fixture
def client() -> Iterator[TestClient]:
    sessions = [
        EngineSession(
            started_at=10.0,
            stopped_at=15.5,
            duration_seconds=5.5,
        )
    ]
    service = EngineHoursService(InMemoryEngineHoursRepository(sessions))
    app.dependency_overrides[get_engine_hours_service] = lambda: service

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_root_returns_api_status(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "name": "Links Connect",
        "version": "0.1.0-alpha.1",
        "status": "running",
    }


def test_health_returns_healthy(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_engine_hours_returns_sessions_from_service(client: TestClient) -> None:
    response = client.get("/engine-hours")

    assert response.status_code == 200
    assert response.json() == [
        {
            "started_at": 10.0,
            "stopped_at": 15.5,
            "duration_seconds": 5.5,
        }
    ]


def test_swagger_openapi_schema_is_available(client: TestClient) -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert response.json()["info"]["title"] == "Links Connect API"
