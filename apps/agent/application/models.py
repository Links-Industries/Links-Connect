from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MachineDashboard:
    machine_id: int
    machine_name: str
    manufacturer: str
    model: str
    total_engine_hours: float
    last_session_duration: float
    next_service_hour: float
    remaining_service_hours: float
    service_due: bool
