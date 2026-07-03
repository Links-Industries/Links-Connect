from __future__ import annotations

from datetime import UTC, datetime

from apps.agent.application import MachineService
from apps.agent.machines.models import Machine
from apps.agent.machines.repository import MachineRepository


class InMemoryMachineRepository(MachineRepository):
    def __init__(self) -> None:
        self.created_machine: Machine | None = None
        self.machine = Machine(
            id=1,
            name="Fairway Mower 1",
            manufacturer="Toro",
            model="Reelmaster 5010-H",
            serial_number="TORO-001",
            year=2024,
            location="Links Golf Club",
            created_at=datetime(2026, 7, 3, tzinfo=UTC),
            updated_at=datetime(2026, 7, 3, tzinfo=UTC),
        )

    def create_machine(self, machine: Machine) -> Machine:
        self.created_machine = machine
        return Machine(
            id=1,
            name=machine.name,
            manufacturer=machine.manufacturer,
            model=machine.model,
            serial_number=machine.serial_number,
            year=machine.year,
            location=machine.location,
            created_at=machine.created_at,
            updated_at=machine.updated_at,
        )

    def get_machine(self, machine_id: int) -> Machine | None:
        if machine_id == self.machine.id:
            return self.machine

        return None

    def list_machines(self) -> list[Machine]:
        return [self.machine]

    def update_machine(self, machine: Machine) -> Machine:
        return machine


def fixed_now() -> datetime:
    return datetime(2026, 7, 3, 12, 0, tzinfo=UTC)


def test_create_machine_builds_machine_and_delegates_to_repository() -> None:
    repository = InMemoryMachineRepository()
    service = MachineService(repository, clock=fixed_now)

    machine = service.create_machine(
        name="Fairway Mower 1",
        manufacturer="Toro",
        model="Reelmaster 5010-H",
        serial_number="TORO-001",
        year=2024,
        location="Links Golf Club",
    )

    assert machine.id == 1
    assert repository.created_machine is not None
    assert repository.created_machine.id is None
    assert repository.created_machine.created_at == fixed_now()
    assert repository.created_machine.updated_at == fixed_now()


def test_get_machine_delegates_to_repository() -> None:
    service = MachineService(InMemoryMachineRepository(), clock=fixed_now)

    machine = service.get_machine(1)

    assert machine is not None
    assert machine.serial_number == "TORO-001"


def test_list_machines_delegates_to_repository() -> None:
    service = MachineService(InMemoryMachineRepository(), clock=fixed_now)

    machines = service.list_machines()

    assert len(machines) == 1
    assert machines[0].name == "Fairway Mower 1"
