from __future__ import annotations

from collections.abc import Iterator

import pytest

from apps.agent.engine_hours.counter import EngineHoursCounter
from apps.agent.engine_hours.exceptions import (
    EngineAlreadyRunningError,
    EngineNotRunningError,
)
from apps.agent.engine_hours.models import EngineSession


def monotonic_values(*values: float) -> Iterator[float]:
    yield from values


def test_new_counter_is_not_running() -> None:
    counter = EngineHoursCounter()

    assert counter.is_running() is False


def test_start_changes_running_state(monkeypatch: pytest.MonkeyPatch) -> None:
    values = monotonic_values(10.0)
    monkeypatch.setattr(
        "apps.agent.engine_hours.counter.time.monotonic",
        lambda: next(values),
    )
    counter = EngineHoursCounter()

    counter.start()

    assert counter.is_running() is True


def test_start_twice_raises_engine_already_running_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    values = monotonic_values(10.0)
    monkeypatch.setattr(
        "apps.agent.engine_hours.counter.time.monotonic",
        lambda: next(values),
    )
    counter = EngineHoursCounter()
    counter.start()

    with pytest.raises(EngineAlreadyRunningError):
        counter.start()


def test_stop_before_start_raises_engine_not_running_error() -> None:
    counter = EngineHoursCounter()

    with pytest.raises(EngineNotRunningError):
        counter.stop()


def test_stop_after_start_returns_engine_session(monkeypatch: pytest.MonkeyPatch) -> None:
    values = monotonic_values(10.0, 15.5)
    monkeypatch.setattr(
        "apps.agent.engine_hours.counter.time.monotonic",
        lambda: next(values),
    )
    counter = EngineHoursCounter()

    counter.start()
    session = counter.stop()

    assert isinstance(session, EngineSession)
    assert session.started_at == 10.0
    assert session.stopped_at == 15.5


def test_engine_session_duration_seconds_is_greater_than_or_equal_to_zero(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    values = monotonic_values(10.0, 10.0)
    monkeypatch.setattr(
        "apps.agent.engine_hours.counter.time.monotonic",
        lambda: next(values),
    )
    counter = EngineHoursCounter()

    counter.start()
    session = counter.stop()

    assert session.duration_seconds >= 0.0


def test_stop_resets_running_state(monkeypatch: pytest.MonkeyPatch) -> None:
    values = monotonic_values(10.0, 12.0)
    monkeypatch.setattr(
        "apps.agent.engine_hours.counter.time.monotonic",
        lambda: next(values),
    )
    counter = EngineHoursCounter()

    counter.start()
    counter.stop()

    assert counter.is_running() is False


def test_starting_second_session_after_stopping_first_works_correctly(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    values = monotonic_values(10.0, 12.0, 20.0, 23.5)
    monkeypatch.setattr(
        "apps.agent.engine_hours.counter.time.monotonic",
        lambda: next(values),
    )
    counter = EngineHoursCounter()

    counter.start()
    first_session = counter.stop()
    counter.start()
    second_session = counter.stop()

    assert first_session.duration_seconds == 2.0
    assert second_session.duration_seconds == 3.5
    assert counter.is_running() is False
