from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from apps.agent.application import EngineHoursService
from apps.api.dependencies import get_engine_hours_service

router = APIRouter(tags=["engine-hours"])


class EngineSessionResponse(BaseModel):
    started_at: float
    stopped_at: float
    duration_seconds: float


@router.get("/engine-hours", response_model=list[EngineSessionResponse])
def engine_hours(
    service: EngineHoursService = Depends(get_engine_hours_service),
) -> list[EngineSessionResponse]:
    return [
        EngineSessionResponse(
            started_at=session.started_at,
            stopped_at=session.stopped_at,
            duration_seconds=session.duration_seconds,
        )
        for session in service.load_sessions()
    ]
