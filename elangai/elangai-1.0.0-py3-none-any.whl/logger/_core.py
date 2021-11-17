# Copyright 2021 elangai Developer. All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
#
# Written by Resha Al-Fahsi <resha.alfahsi@techbros.io>, 2021.
# =========================================================================


import logging

from pathlib import Path
from logging.handlers import SysLogHandler
from os.path import dirname, join, expanduser
from elangai.__about__ import __title__ as NAME
from datetime import date


LOGGING_LEVEL = {'INFO': logging.INFO,
                 'WARNING': logging.WARNING,
                 'ERROR': logging.ERROR,
                 'DEBUG': logging.DEBUG,
                 'CRITICAL': logging.CRITICAL}


class CoreLogger:
    """elangai core logger.
    """
    def __init__(self):
        fmt = '%(asctime)s - %(name)s: [%(levelname)s] %(message)s'
        self._handler_format = logging.Formatter(fmt)

        log_file = join(expanduser('~'), '.elangai/log')
        Path(log_file).mkdir(parents=True, exist_ok=True)
        self._log_file = join(log_file, '{}.txt'.format(str(date.today()).replace('-', '_')))

    @classmethod
    def scream(cls, log_message, level=LOGGING_LEVEL['INFO']):
        """Instant logger.
        
        :param log_message: message to display in logger
        :param level: log message level
        """
        logger = cls()
        return logger.screech(log_message, level)       

    def screech(self, log_message, level=LOGGING_LEVEL['INFO']):
        """The function to print log message.

        :param log_message: message to display in logger
        :param level: log message level
        """
        handlers = [SysLogHandler(address='/dev/log'), logging.FileHandler(self._log_file), logging.StreamHandler()]
        key_list = list(LOGGING_LEVEL.keys())
        value_list = list(LOGGING_LEVEL.values())

        for handler in handlers:
            handler.setFormatter(self._handler_format)
            logger = logging.getLogger(NAME)
            logger.addHandler(handler)
            logger.propagate = False
            logger.setLevel(level)
            getattr(logger, key_list[value_list.index(level)].lower())(log_message)
            logger.handlers.clear()
