from __future__ import annotations

from fastapi import FastAPI

from .routers import engine_hours, health, machines

API_NAME = "Links Connect"
API_VERSION = "0.1.0-alpha.1"
API_STATUS = "running"


def create_app() -> FastAPI:
    application = FastAPI(title=f"{API_NAME} API", version=API_VERSION)

    @application.get("/", tags=["root"])
    def root() -> dict[str, str]:
        return {
            "name": API_NAME,
            "version": API_VERSION,
            "status": API_STATUS,
        }

    application.include_router(health.router)
    application.include_router(engine_hours.router)
    application.include_router(machines.router)
    return application


app = create_app()
