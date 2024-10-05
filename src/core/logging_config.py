import logging.config
from typing import Any


default_log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "{asctime} | {levelname} | {filename} | line {lineno} | {message}",
            "style": "{",
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "default": {
            "level": "INFO",
            "handlers": ["default"],
            "propagate": False,
        },
    },
}


async def setup_logging(logging_config: dict[str, Any] | None = None) -> None:
    logging.config.dictConfig(logging_config or default_log_config)
