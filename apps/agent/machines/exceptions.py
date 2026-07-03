from __future__ import annotations


class MachineRegistryError(Exception):
    pass


class MachineNotFoundError(MachineRegistryError):
    pass


class MachineIdRequiredError(MachineRegistryError):
    pass
