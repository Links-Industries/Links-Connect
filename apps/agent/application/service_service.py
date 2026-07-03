from __future__ import annotations

from apps.agent.service.monitor import ServiceMonitor
from apps.agent.service.policies import ServicePolicy


class ServiceService:
    def get_remaining_hours(
        self,
        total_engine_hours: float,
        policy: ServicePolicy,
    ) -> float:
        return ServiceMonitor(total_engine_hours, policy).remaining_hours()

    def is_service_due(
        self,
        total_engine_hours: float,
        policy: ServicePolicy,
    ) -> bool:
        return ServiceMonitor(total_engine_hours, policy).is_service_due()
