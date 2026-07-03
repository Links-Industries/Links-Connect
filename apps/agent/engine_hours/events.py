from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class EngineStarted:
    machine_id: int
    occurred_at: datetime


@dataclass(frozen=True, slots=True)
class EngineStopped:
    machine_id: int
    occurred_at: datetime


@dataclass(frozen=True, slots=True)
class EngineHoursChanged:
    machine_id: int
    total_seconds: int
    occurred_at: datetime
