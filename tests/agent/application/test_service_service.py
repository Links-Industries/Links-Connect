from __future__ import annotations

from apps.agent.application import ServiceService
from apps.agent.service import ServicePolicy


def test_get_remaining_hours_uses_service_monitor() -> None:
    service = ServiceService()

    remaining_hours = service.get_remaining_hours(
        total_engine_hours=125.0,
        policy=ServicePolicy(interval_hours=250.0),
    )

    assert remaining_hours == 125.0


def test_is_service_due_uses_service_monitor() -> None:
    service = ServiceService()

    assert service.is_service_due(
        total_engine_hours=250.0,
        policy=ServicePolicy(interval_hours=250.0),
    ) is True
