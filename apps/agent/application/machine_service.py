from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime

from apps.agent.machines.models import Machine
from apps.agent.machines.repository import MachineRepository


class MachineService:
    def __init__(
        self,
        repository: MachineRepository,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._repository = repository
        self._clock = clock if clock is not None else self._utc_now

    def create_machine(
        self,
        name: str,
        manufacturer: str,
        model: str,
        serial_number: str,
        year: int,
        location: str,
    ) -> Machine:
        now = self._clock()
        machine = Machine(
            id=None,
            name=name,
            manufacturer=manufacturer,
            model=model,
            serial_number=serial_number,
            year=year,
            location=location,
            created_at=now,
            updated_at=now,
        )

        return self._repository.create_machine(machine)

    def get_machine(self, machine_id: int) -> Machine | None:
        return self._repository.get_machine(machine_id)

    def list_machines(self) -> list[Machine]:
        return self._repository.list_machines()

    @staticmethod
    def _utc_now() -> datetime:
        return datetime.now(UTC)
