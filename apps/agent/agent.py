from __future__ import annotations

import logging

from .config import Configuration


class LinksAgent:
    def __init__(self, configuration: Configuration) -> None:
        self._configuration = configuration
        self._logger = logging.getLogger(__name__)
        self._started = False

    def start(self) -> None:
        self._logger.info(
            "Starting %s in %s mode",
            self._configuration.app_name,
            self._configuration.environment,
        )
        self._logger.debug(
            "Plugin directory configured: %s",
            self._configuration.plugin_directory,
        )
        self._started = True
        self._logger.info("%s started", self._configuration.app_name)

    def shutdown(self) -> None:
        if not self._started:
            self._logger.debug("Shutdown requested before startup completed")
            return

        self._logger.info("Shutting down %s", self._configuration.app_name)
        self._started = False
        self._logger.info("%s stopped", self._configuration.app_name)
