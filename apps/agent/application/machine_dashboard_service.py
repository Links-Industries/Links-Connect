from __future__ import annotations

from apps.agent.machines.exceptions import MachineNotFoundError
from apps.agent.service.policies import ServicePolicy

from .engine_hours_service import EngineHoursService
from .machine_service import MachineService
from .models import MachineDashboard
from .service_service import ServiceService


class MachineDashboardService:
    def __init__(
        self,
        machine_service: MachineService,
        engine_hours_service: EngineHoursService,
        service_service: ServiceService,
        service_policy: ServicePolicy,
    ) -> None:
        self._machine_service = machine_service
        self._engine_hours_service = engine_hours_service
        self._service_service = service_service
        self._service_policy = service_policy

    def get_dashboard(self, machine_id: int) -> MachineDashboard:
        machine = self._machine_service.get_machine(machine_id)

        if machine is None or machine.id is None:
            raise MachineNotFoundError(f"Machine {machine_id} was not found.")

        total_engine_hours = self._engine_hours_service.total_engine_hours()

        return MachineDashboard(
            machine_id=machine.id,
            machine_name=machine.name,
            manufacturer=machine.manufacturer,
            model=machine.model,
            total_engine_hours=total_engine_hours,
            last_session_duration=self._engine_hours_service.last_session_duration(),
            next_service_hour=self._service_service.get_next_service_hour(
                total_engine_hours,
                self._service_policy,
            ),
            remaining_service_hours=self._service_service.get_remaining_hours(
                total_engine_hours,
                self._service_policy,
            ),
            service_due=self._service_service.is_service_due(
                total_engine_hours,
                self._service_policy,
            ),
        )
