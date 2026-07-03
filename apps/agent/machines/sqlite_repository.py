from __future__ import annotations

import sqlite3
from dataclasses import replace
from datetime import datetime

from apps.agent.infrastructure import Database

from .exceptions import MachineIdRequiredError, MachineNotFoundError
from .models import Machine
from .repository import MachineRepository


INSERT_MACHINE_SQL = """
INSERT INTO machines (
    name,
    manufacturer,
    model,
    serial_number,
    year,
    location,
    created_at,
    updated_at
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

SELECT_MACHINE_SQL = """
SELECT id, name, manufacturer, model, serial_number, year, location, created_at, updated_at
FROM machines
WHERE id = ?
"""

SELECT_MACHINES_SQL = """
SELECT id, name, manufacturer, model, serial_number, year, location, created_at, updated_at
FROM machines
ORDER BY id ASC
"""

UPDATE_MACHINE_SQL = """
UPDATE machines
SET
    name = ?,
    manufacturer = ?,
    model = ?,
    serial_number = ?,
    year = ?,
    location = ?,
    updated_at = ?
WHERE id = ?
"""


class SQLiteMachineRepository(MachineRepository):
    def __init__(self, database: Database) -> None:
        self._database = database

    def create_machine(self, machine: Machine) -> Machine:
        with self._database.connect() as connection:
            cursor = connection.execute(
                INSERT_MACHINE_SQL,
                (
                    machine.name,
                    machine.manufacturer,
                    machine.model,
                    machine.serial_number,
                    machine.year,
                    machine.location,
                    machine.created_at.isoformat(),
                    machine.updated_at.isoformat(),
                ),
            )
            machine_id = int(cursor.lastrowid)

        return replace(machine, id=machine_id)

    def get_machine(self, machine_id: int) -> Machine | None:
        with self._database.connect() as connection:
            row = connection.execute(SELECT_MACHINE_SQL, (machine_id,)).fetchone()

        if row is None:
            return None

        return self._map_row(row)

    def list_machines(self) -> list[Machine]:
        with self._database.connect() as connection:
            rows = connection.execute(SELECT_MACHINES_SQL).fetchall()

        return [self._map_row(row) for row in rows]

    def update_machine(self, machine: Machine) -> Machine:
        if machine.id is None:
            raise MachineIdRequiredError("Machine id is required for updates.")

        with self._database.connect() as connection:
            cursor = connection.execute(
                UPDATE_MACHINE_SQL,
                (
                    machine.name,
                    machine.manufacturer,
                    machine.model,
                    machine.serial_number,
                    machine.year,
                    machine.location,
                    machine.updated_at.isoformat(),
                    machine.id,
                ),
            )

        if cursor.rowcount == 0:
            raise MachineNotFoundError(f"Machine {machine.id} was not found.")

        return machine

    @staticmethod
    def _map_row(row: sqlite3.Row) -> Machine:
        return Machine(
            id=int(row["id"]),
            name=str(row["name"]),
            manufacturer=str(row["manufacturer"]),
            model=str(row["model"]),
            serial_number=str(row["serial_number"]),
            year=int(row["year"]),
            location=str(row["location"]),
            created_at=datetime.fromisoformat(str(row["created_at"])),
            updated_at=datetime.fromisoformat(str(row["updated_at"])),
        )
