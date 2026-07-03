from __future__ import annotations

import math

from .exceptions import InvalidEngineHoursError
from .policies import ServicePolicy


class ServiceMonitor:
    def __init__(self, total_engine_hours: float, policy: ServicePolicy) -> None:
        if total_engine_hours < 0:
            raise InvalidEngineHoursError("Total engine hours cannot be negative.")

        self._total_engine_hours = total_engine_hours
        self._policy = policy

    def remaining_hours(self) -> float:
        return max(self.next_service_hour() - self._total_engine_hours, 0.0)

    def is_service_due(self) -> bool:
        if self._total_engine_hours == 0:
            return False

        return math.isclose(self.remaining_hours(), 0.0, abs_tol=1e-9)

    def next_service_hour(self) -> float:
        interval_hours = self._policy.interval_hours
        completed_intervals = math.floor(self._total_engine_hours / interval_hours)
        service_hour = completed_intervals * interval_hours

        if service_hour > 0 and math.isclose(
            self._total_engine_hours,
            service_hour,
            abs_tol=1e-9,
        ):
            return service_hour

        return (completed_intervals + 1) * interval_hours
