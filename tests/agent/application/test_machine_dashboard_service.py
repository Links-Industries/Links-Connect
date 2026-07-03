from __future__ import annotations

from datetime import UTC, datetime

import pytest

from apps.agent.application import (
    EngineHoursService,
    MachineDashboard,
    MachineDashboardService,
    MachineService,
    ServiceService,
)
from apps.agent.engine_hours.models import EngineSession
from apps.agent.engine_hours.repository import EngineHoursRepository
from apps.agent.machines.exceptions import MachineNotFoundError
from apps.agent.machines.models import Machine
from apps.agent.machines.repository import MachineRepository
from apps.agent.service import ServicePolicy


class InMemoryMachineRepository(MachineRepository):
    def __init__(self, machine: Machine | None) -> None:
        self._machine = machine

    def create_machine(self, machine: Machine) -> Machine:
        return machine

    def get_machine(self, machine_id: int) -> Machine | None:
        if self._machine is not None and self._machine.id == machine_id:
            return self._machine

        return None

    def list_machines(self) -> list[Machine]:
        if self._machine is None:
            return []

        return [self._machine]

    def update_machine(self, machine: Machine) -> Machine:
        self._machine = machine
        return machine


class InMemoryEngineHoursRepository(EngineHoursRepository):
    def __init__(self, sessions: list[EngineSession]) -> None:
        self._sessions = sessions

    def save_session(self, session: EngineSession) -> None:
        self._sessions.append(session)

    def load_sessions(self) -> list[EngineSession]:
        return list(self._sessions)


def build_machine() -> Machine:
    now = datetime(2026, 7, 3, tzinfo=UTC)
    return Machine(
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


def build_dashboard_service(
    machine: Machine | None,
    sessions: list[EngineSession],
    policy: ServicePolicy | None = None,
) -> MachineDashboardService:
    return MachineDashboardService(
        machine_service=MachineService(InMemoryMachineRepository(machine)),
        engine_hours_service=EngineHoursService(InMemoryEngineHoursRepository(sessions)),
        service_service=ServiceService(),
        service_policy=policy if policy is not None else ServicePolicy(interval_hours=250.0),
    )


def test_get_dashboard_aggregates_machine_engine_hours_and_service_status() -> None:
    sessions = [
        EngineSession(started_at=10.0, stopped_at=3610.0, duration_seconds=3600.0),
        EngineSession(started_at=4000.0, stopped_at=5800.0, duration_seconds=1800.0),
    ]
    service = build_dashboard_service(build_machine(), sessions)

    dashboard = service.get_dashboard(1)

    assert dashboard == MachineDashboard(
        machine_id=1,
        machine_name="Fairway Mower 1",
        manufacturer="Toro",
        model="Reelmaster 5010-H",
        total_engine_hours=1.5,
        last_session_duration=1800.0,
        next_service_hour=250.0,
        remaining_service_hours=248.5,
        service_due=False,
    )


def test_get_dashboard_reports_service_due_at_policy_boundary() -> None:
    sessions = [
        EngineSession(started_at=0.0, stopped_at=900000.0, duration_seconds=900000.0),
    ]
    service = build_dashboard_service(build_machine(), sessions)

    dashboard = service.get_dashboard(1)

    assert dashboard.total_engine_hours == 250.0
    assert dashboard.next_service_hour == 250.0
    assert dashboard.remaining_service_hours == 0.0
    assert dashboard.service_due is True


def test_get_dashboard_supports_configurable_service_policy() -> None:
    sessions = [
        EngineSession(started_at=0.0, stopped_at=3600.0, duration_seconds=3600.0),
    ]
    service = build_dashboard_service(
        build_machine(),
        sessions,
        policy=ServicePolicy(interval_hours=500.0),
    )

    dashboard = service.get_dashboard(1)

    assert dashboard.next_service_hour == 500.0
    assert dashboard.remaining_service_hours == 499.0


def test_get_dashboard_raises_when_machine_does_not_exist() -> None:
    service = build_dashboard_service(machine=None, sessions=[])

    with pytest.raises(MachineNotFoundError):
        service.get_dashboard(1)
