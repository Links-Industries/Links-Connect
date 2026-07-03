from __future__ import annotations

from collections.abc import Iterator
from dataclasses import replace
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient

from apps.agent.application import MachineService
from apps.agent.machines.models import Machine
from apps.agent.machines.repository import MachineRepository
from apps.api.dependencies import get_machine_service
from apps.api.main import app


class InMemoryMachineRepository(MachineRepository):
    def __init__(self) -> None:
        self._machines: dict[int, Machine] = {}
        self._next_id = 1

    def create_machine(self, machine: Machine) -> Machine:
        machine_id = self._next_id
        self._next_id += 1
        created = replace(machine, id=machine_id)
        self._machines[machine_id] = created
        return created

    def get_machine(self, machine_id: int) -> Machine | None:
        return self._machines.get(machine_id)

    def list_machines(self) -> list[Machine]:
        return list(self._machines.values())

    def update_machine(self, machine: Machine) -> Machine:
        if machine.id is None:
            raise ValueError("Machine id is required.")

        self._machines[machine.id] = machine
        return machine


@pytest.fixture
def machine_repository() -> InMemoryMachineRepository:
    return InMemoryMachineRepository()


def fixed_now() -> datetime:
    return datetime(2026, 7, 3, 12, 0, tzinfo=UTC)


@pytest.fixture
def client(machine_repository: InMemoryMachineRepository) -> Iterator[TestClient]:
    service = MachineService(machine_repository, clock=fixed_now)
    app.dependency_overrides[get_machine_service] = lambda: service

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def machine_payload(serial_number: str = "TORO-001") -> dict[str, object]:
    return {
        "name": "Fairway Mower 1",
        "manufacturer": "Toro",
        "model": "Reelmaster 5010-H",
        "serial_number": serial_number,
        "year": 2024,
        "location": "Links Golf Club",
    }


def existing_machine() -> Machine:
    now = datetime(2026, 7, 3, 10, 0, tzinfo=UTC)
    return Machine(
        id=None,
        name="Utility Vehicle 1",
        manufacturer="Club Car",
        model="Carryall 700",
        serial_number="CLUBCAR-001",
        year=2023,
        location="Maintenance Yard",
        created_at=now,
        updated_at=now,
    )


def test_post_machines_creates_machine(client: TestClient) -> None:
    response = client.post("/machines", json=machine_payload())

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["name"] == "Fairway Mower 1"
    assert body["manufacturer"] == "Toro"
    assert body["model"] == "Reelmaster 5010-H"
    assert body["serial_number"] == "TORO-001"
    assert body["year"] == 2024
    assert body["location"] == "Links Golf Club"
    assert body["created_at"].startswith("2026-07-03T12:00:00")
    assert body["updated_at"].startswith("2026-07-03T12:00:00")


def test_get_machines_returns_all_machines(
    client: TestClient,
    machine_repository: InMemoryMachineRepository,
) -> None:
    created = machine_repository.create_machine(existing_machine())

    response = client.get("/machines")

    assert response.status_code == 200
    assert response.json()[0]["id"] == created.id
    assert response.json()[0]["serial_number"] == "CLUBCAR-001"


def test_get_machine_by_id_returns_machine(
    client: TestClient,
    machine_repository: InMemoryMachineRepository,
) -> None:
    created = machine_repository.create_machine(existing_machine())

    response = client.get(f"/machines/{created.id}")

    assert response.status_code == 200
    assert response.json()["id"] == created.id
    assert response.json()["name"] == "Utility Vehicle 1"


def test_get_machine_by_id_returns_404_when_missing(client: TestClient) -> None:
    response = client.get("/machines/404")

    assert response.status_code == 404
    assert response.json() == {"detail": "Machine not found."}
