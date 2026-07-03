from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Machine:
    id: int | None
    name: str
    manufacturer: str
    model: str
    serial_number: str
    year: int
    location: str
    created_at: datetime
    updated_at: datetime
