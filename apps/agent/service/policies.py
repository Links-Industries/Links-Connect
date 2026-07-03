from __future__ import annotations

from dataclasses import dataclass

from .exceptions import InvalidServicePolicyError


@dataclass(frozen=True, slots=True)
class ServicePolicy:
    interval_hours: float

    def __post_init__(self) -> None:
        if self.interval_hours <= 0:
            raise InvalidServicePolicyError(
                "Service interval must be greater than zero hours."
            )
