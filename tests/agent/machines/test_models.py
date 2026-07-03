from __future__ import annotations

from datetime import UTC, datetime

from apps.agent.machines.models import Machine


def test_machine_model_contains_registry_fields() -> None:
    now = datetime(2026, 7, 3, tzinfo=UTC)

    machine = Machine(
        id=1,
        name="Fairway Mower 1",
        manufacturer="Toro",
        model="Reelmaster 5010-H",
        serial_number="TORO-001",
        year=2024,
        location="Links Golf Club",
        created_at=now,
        updated_at=now,
    )

    assert machine.id == 1
    assert machine.name == "Fairway Mower 1"
    assert machine.manufacturer == "Toro"
    assert machine.model == "Reelmaster 5010-H"
    assert machine.serial_number == "TORO-001"
    assert machine.year == 2024
    assert machine.location == "Links Golf Club"
    assert machine.created_at == now
    assert machine.updated_at == now
