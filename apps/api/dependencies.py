from __future__ import annotations

from functools import lru_cache

from apps.agent.application import EngineHoursService, MachineService, ServiceService
from apps.agent.config import Configuration
from apps.agent.engine_hours.repository import EngineHoursRepository
from apps.agent.engine_hours.sqlite_repository import SQLiteEngineHoursRepository
from apps.agent.infrastructure import Database
from apps.agent.machines.repository import MachineRepository
from apps.agent.machines.sqlite_repository import SQLiteMachineRepository


@lru_cache(maxsize=1)
def get_database() -> Database:
    configuration = Configuration.load()
    database = Database(configuration.database_path)
    database.initialize_schema()
    return database


def get_engine_hours_repository() -> EngineHoursRepository:
    return SQLiteEngineHoursRepository(get_database())


def get_machine_repository() -> MachineRepository:
    return SQLiteMachineRepository(get_database())


def get_engine_hours_service() -> EngineHoursService:
    return EngineHoursService(get_engine_hours_repository())


def get_machine_service() -> MachineService:
    return MachineService(get_machine_repository())


def get_service_service() -> ServiceService:
    return ServiceService()
