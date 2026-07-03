from __future__ import annotations


class EngineHoursError(Exception):
    pass


class EngineAlreadyRunningError(EngineHoursError):
    pass


class EngineNotRunningError(EngineHoursError):
    pass
