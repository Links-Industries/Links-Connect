from __future__ import annotations

import logging
import sys


LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"


def configure_logging(log_level: str) -> None:
    logging.basicConfig(
        level=log_level,
        format=LOG_FORMAT,
        stream=sys.stdout,
        force=True,
    )
