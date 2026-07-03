from __future__ import annotations

import pytest

from apps.agent.service import (
    InvalidEngineHoursError,
    InvalidServicePolicyError,
    ServiceMonitor,
    ServicePolicy,
)


def test_remaining_hours_for_250_hour_interval() -> None:
    monitor = ServiceMonitor(
        total_engine_hours=125.0,
        policy=ServicePolicy(interval_hours=250.0),
    )

    assert monitor.remaining_hours() == 125.0
    assert monitor.next_service_hour() == 250.0


def test_remaining_hours_for_500_hour_interval() -> None:
    monitor = ServiceMonitor(
        total_engine_hours=125.0,
        policy=ServicePolicy(interval_hours=500.0),
    )

    assert monitor.remaining_hours() == 375.0
    assert monitor.next_service_hour() == 500.0


def test_service_is_due_at_exact_service_boundary() -> None:
    monitor = ServiceMonitor(
        total_engine_hours=250.0,
        policy=ServicePolicy(interval_hours=250.0),
    )

    assert monitor.is_service_due() is True
    assert monitor.remaining_hours() == 0.0
    assert monitor.next_service_hour() == 250.0


def test_service_is_not_due_before_service_boundary() -> None:
    monitor = ServiceMonitor(
        total_engine_hours=249.0,
        policy=ServicePolicy(interval_hours=250.0),
    )

    assert monitor.is_service_due() is False
    assert monitor.remaining_hours() == 1.0
    assert monitor.next_service_hour() == 250.0


def test_zero_engine_hours_is_not_service_due() -> None:
    monitor = ServiceMonitor(
        total_engine_hours=0.0,
        policy=ServicePolicy(interval_hours=250.0),
    )

    assert monitor.is_service_due() is False
    assert monitor.remaining_hours() == 250.0
    assert monitor.next_service_hour() == 250.0


def test_next_service_hour_moves_to_next_interval_after_boundary() -> None:
    monitor = ServiceMonitor(
        total_engine_hours=251.0,
        policy=ServicePolicy(interval_hours=250.0),
    )

    assert monitor.is_service_due() is False
    assert monitor.remaining_hours() == 249.0
    assert monitor.next_service_hour() == 500.0


def test_service_due_for_500_hour_interval_boundary() -> None:
    monitor = ServiceMonitor(
        total_engine_hours=1000.0,
        policy=ServicePolicy(interval_hours=500.0),
    )

    assert monitor.is_service_due() is True
    assert monitor.remaining_hours() == 0.0
    assert monitor.next_service_hour() == 1000.0


def test_policy_interval_must_be_greater_than_zero() -> None:
    with pytest.raises(InvalidServicePolicyError):
        ServicePolicy(interval_hours=0.0)


def test_total_engine_hours_cannot_be_negative() -> None:
    with pytest.raises(InvalidEngineHoursError):
        ServiceMonitor(
            total_engine_hours=-1.0,
            policy=ServicePolicy(interval_hours=250.0),
        )
