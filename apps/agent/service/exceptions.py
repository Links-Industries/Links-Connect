from __future__ import annotations


class ServiceMonitorError(Exception):
    pass


class InvalidServicePolicyError(ServiceMonitorError):
    pass


class InvalidEngineHoursError(ServiceMonitorError):
    pass
