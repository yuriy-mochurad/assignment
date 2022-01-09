# -*- coding: utf-8 -*-
import os
import structlog
import logging
import logging.config
import datetime

timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S")
pre_chain = [
    timestamper,
    structlog.stdlib.add_log_level,
]

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "file": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(colors=False),
            "foreign_pre_chain": pre_chain,
        }
    },
    "handlers": {
        "file": {
            "()": logging.FileHandler,
            "filename": os.path.join(
                os.getcwd(), "tmp", "logs", "log-" + f"{datetime.datetime.now()}.log"
            ),
            "formatter": "file",
        },
    },
    "loggers": {
        "": {
            "handlers": ["file"],
            "level": "INFO",
        }
    },
}


def get_log(log_name):
    if not os.path.exists(os.path.join(os.path.join(os.getcwd(), "tmp", "logs"))):
        os.makedirs(os.path.join(os.getcwd(), "tmp", "logs"))
    logging.config.dictConfig(LOGGING_CONFIG)
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
    )
    return structlog.get_logger(log_name)
