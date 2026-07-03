from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class EngineHours:
    id: int | None
    machine_id: int
    total_seconds: int
    updated_at: datetime


@dataclass(frozen=True, slots=True)
class EngineSession:
    started_at: float
    stopped_at: float
    duration_seconds: float
