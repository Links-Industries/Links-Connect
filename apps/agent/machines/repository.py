from __future__ import annotations

from abc import ABC, abstractmethod

from .models import Machine


class MachineRepository(ABC):
    @abstractmethod
    def create_machine(self, machine: Machine) -> Machine:
        raise NotImplementedError

    @abstractmethod
    def get_machine(self, machine_id: int) -> Machine | None:
        raise NotImplementedError

    @abstractmethod
    def list_machines(self) -> list[Machine]:
        raise NotImplementedError

    @abstractmethod
    def update_machine(self, machine: Machine) -> Machine:
        raise NotImplementedError
