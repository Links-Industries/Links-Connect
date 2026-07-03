from __future__ import annotations

from dataclasses import dataclass

from .policies import ServicePolicy


@dataclass(frozen=True, slots=True)
class ServiceStatus:
    total_engine_hours: float
    policy: ServicePolicy
    remaining_hours: float
    next_service_hour: float
    is_service_due: bool
