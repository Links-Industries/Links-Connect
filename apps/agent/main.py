from __future__ import annotations

import logging

from .agent import LinksAgent
from .config import DEFAULT_LOG_LEVEL, Configuration
from .infrastructure import Database
from .logger import configure_logging


def main() -> int:
    configure_logging(DEFAULT_LOG_LEVEL)
    logger = logging.getLogger(__name__)
    agent: LinksAgent | None = None

    try:
        logger.info("Links Agent starting")
        configuration = Configuration.load()
        configure_logging(configuration.log_level)
        logger = logging.getLogger(__name__)
        logger.info("Configuration loaded")

        database = Database(configuration.database_path)
        database.initialize_schema()
        logger.info("Database initialized at %s", database.database_path)

        agent = LinksAgent(configuration)
        agent.start()
        return 0
    except KeyboardInterrupt:
        logger.info("Links Agent interrupted")
        return 130
    except Exception:
        logger.exception("Links Agent failed during startup")
        return 1
    finally:
        if agent is not None:
            agent.shutdown()
        logging.shutdown()
