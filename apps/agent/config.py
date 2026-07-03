from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Self


DEFAULT_APP_NAME = "Links Agent"
DEFAULT_ENVIRONMENT = "production"
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_PLUGIN_DIRECTORY = Path("plugins")
DEFAULT_DATABASE_PATH = Path("data") / "links_connect.db"


@dataclass(frozen=True, slots=True)
class Configuration:
    app_name: str = DEFAULT_APP_NAME
    environment: str = DEFAULT_ENVIRONMENT
    log_level: str = DEFAULT_LOG_LEVEL
    plugin_directory: Path = DEFAULT_PLUGIN_DIRECTORY
    database_path: Path = DEFAULT_DATABASE_PATH

    @classmethod
    def load(cls, environment: Mapping[str, str] | None = None) -> Self:
        source = environment if environment is not None else os.environ

        log_level = source.get("LINKS_AGENT_LOG_LEVEL", DEFAULT_LOG_LEVEL).upper()
        cls._validate_log_level(log_level)

        return cls(
            app_name=source.get("LINKS_AGENT_APP_NAME", DEFAULT_APP_NAME),
            environment=source.get("LINKS_AGENT_ENVIRONMENT", DEFAULT_ENVIRONMENT),
            log_level=log_level,
            plugin_directory=Path(
                source.get("LINKS_AGENT_PLUGIN_DIRECTORY", str(DEFAULT_PLUGIN_DIRECTORY))
            ),
            database_path=Path(
                source.get("LINKS_AGENT_DATABASE_PATH", str(DEFAULT_DATABASE_PATH))
            ),
        )

    @staticmethod
    def _validate_log_level(log_level: str) -> None:
        if logging.getLevelName(log_level) == f"Level {log_level}":
            supported_levels = "CRITICAL, ERROR, WARNING, INFO, DEBUG"
            msg = (
                f"Unsupported LINKS_AGENT_LOG_LEVEL '{log_level}'. "
                f"Use one of: {supported_levels}."
            )
            raise ValueError(msg)
