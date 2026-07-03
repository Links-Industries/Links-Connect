from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path

import pytest

from apps.agent.infrastructure import Database
from apps.agent.machines.exceptions import MachineIdRequiredError, MachineNotFoundError
from apps.agent.machines.models import Machine
from apps.agent.machines.sqlite_repository import SQLiteMachineRepository


@pytest.fixture
def repository(tmp_path: Path) -> SQLiteMachineRepository:
    database = Database(tmp_path / "links_connect_test.db")
    database.initialize_schema()
    return SQLiteMachineRepository(database)


def build_machine(serial_number: str = "TORO-001") -> Machine:
    now = datetime(2026, 7, 3, 10, 0, tzinfo=UTC)
    return Machine(
        id=None,
        name="Fairway Mower 1",
        manufacturer="Toro",
        model="Reelmaster 5010-H",
        serial_number=serial_number,
        year=2024,
        location="Links Golf Club",
        created_at=now,
        updated_at=now,
    )


def test_create_machine_persists_machine(repository: SQLiteMachineRepository) -> None:
    created = repository.create_machine(build_machine())

    assert created.id is not None
    assert repository.get_machine(created.id) == created


def test_list_machines_returns_all_machines(repository: SQLiteMachineRepository) -> None:
    first = repository.create_machine(build_machine("TORO-001"))
    second = repository.create_machine(build_machine("TORO-002"))

    assert repository.list_machines() == [first, second]


def test_get_machine_returns_none_when_missing(repository: SQLiteMachineRepository) -> None:
    assert repository.get_machine(404) is None


def test_update_machine_persists_changes(repository: SQLiteMachineRepository) -> None:
    created = repository.create_machine(build_machine())
    updated_at = datetime(2026, 7, 3, 11, 0, tzinfo=UTC)
    updated = replace(created, name="Updated Mower", location="Workshop", updated_at=updated_at)

    saved = repository.update_machine(updated)

    assert saved == updated
    assert repository.get_machine(saved.id or 0) == updated


def test_update_machine_requires_id(repository: SQLiteMachineRepository) -> None:
    with pytest.raises(MachineIdRequiredError):
        repository.update_machine(build_machine())


def test_update_machine_raises_when_missing(repository: SQLiteMachineRepository) -> None:
    missing = replace(build_machine(), id=999)

    with pytest.raises(MachineNotFoundError):
        repository.update_machine(missing)
