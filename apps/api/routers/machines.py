from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from apps.agent.application import MachineService
from apps.agent.machines.models import Machine
from apps.api.dependencies import get_machine_service

router = APIRouter(prefix="/machines", tags=["machines"])


class MachineCreateRequest(BaseModel):
    name: str
    manufacturer: str
    model: str
    serial_number: str
    year: int
    location: str


class MachineResponse(BaseModel):
    id: int
    name: str
    manufacturer: str
    model: str
    serial_number: str
    year: int
    location: str
    created_at: datetime
    updated_at: datetime


def _to_response(machine: Machine) -> MachineResponse:
    if machine.id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Machine repository returned an unpersisted machine.",
        )

    return MachineResponse(
        id=machine.id,
        name=machine.name,
        manufacturer=machine.manufacturer,
        model=machine.model,
        serial_number=machine.serial_number,
        year=machine.year,
        location=machine.location,
        created_at=machine.created_at,
        updated_at=machine.updated_at,
    )


@router.get("", response_model=list[MachineResponse])
def list_machines(
    service: MachineService = Depends(get_machine_service),
) -> list[MachineResponse]:
    return [_to_response(machine) for machine in service.list_machines()]


@router.get("/{machine_id}", response_model=MachineResponse)
def get_machine(
    machine_id: int,
    service: MachineService = Depends(get_machine_service),
) -> MachineResponse:
    machine = service.get_machine(machine_id)

    if machine is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Machine not found.",
        )

    return _to_response(machine)


@router.post("", response_model=MachineResponse, status_code=status.HTTP_201_CREATED)
def create_machine(
    request: MachineCreateRequest,
    service: MachineService = Depends(get_machine_service),
) -> MachineResponse:
    machine = service.create_machine(
        name=request.name,
        manufacturer=request.manufacturer,
        model=request.model,
        serial_number=request.serial_number,
        year=request.year,
        location=request.location,
    )

    return _to_response(machine)
