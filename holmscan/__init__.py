# -*- coding: utf-8 -*-

""" holmscan """

# python std lib
import os
import logging
import logging.config
import random
import string
import tempfile

__author__ = "Henrik Holmboe"
__email__ = "henrik@dynamist.se"
__version__ = "0.0.2"
__url__ = "https://github.com/dynamist/holmscan"
__devel__ = True

log_level_to_string_map = {
    5: "DEBUG",
    4: "INFO",
    3: "WARNING",
    2: "ERROR",
    1: "CRITICAL",
    0: "INFO",
}

random_log_file = os.path.join(
    tempfile.gettempdir(),
    "holmscan-"
    + "".join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(12))
    + ".log",
)


def init_logging(log_level):
    """
    Init logging settings with default set to INFO.
    """
    level = log_level_to_string_map[log_level]

    if level in os.environ:
        msg = "%(levelname)s - %(name)s:%(lineno)s - %(message)s"
    else:
        msg = "%(levelname)s - %(message)s"

    logging_conf = {
        "version": 1,
        "root": {"level": level, "handlers": []},
        "loggers": {"holmscan": {"level": "DEBUG", "handlers": ["console"]}},
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": level,
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.FileHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "filename": random_log_file,
            },
        },
        "formatters": {"simple": {"format": " {0}".format(msg)}},
    }

    logging.config.dictConfig(logging_conf)
