# Copyright 2021 elangai Developer. All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
#
# Written by Resha Al-Fahsi <resha.alfahsi@techbros.io>, 2021.
# =========================================================================


from elangai.logger import (
    elangai_logger,
    LOGGING_LEVEL
)


@elangai_logger
class ElangAIWarning:
    """Print warning message.
    
    :param message: message to be printed
    """
    def __call__(self, message: str):
        self.logger(message=message, level=LOGGING_LEVEL['WARNING'])


@elangai_logger
class ElangAIInfo:
    """Print info message.
    
    :param message: message to be printed
    """
    def __call__(self, message: str):
        self.logger(message=message, level=LOGGING_LEVEL['INFO'])


@elangai_logger
class ElangAICritical:
    """Print critical message.
    
    :param message: message to be printed
    """
    def __call__(self, message: str):
        self.logger(message=message, level=LOGGING_LEVEL['CRITICAL'])


@elangai_logger
class ElangAIDebug:
    """Print debug message.
    
    :param message: message to be printed
    """
    def __call__(self, message: str):
        self.logger(message=message, level=LOGGING_LEVEL['DEBUG'])


@elangai_logger
class ElangAIError:
    """Print error message.
    
    :param error: exception being handle
    :param message: messages or arguments to be printed
    :param raise_exception: flag for triggering the exception
    """
    def __call__(self, error: type = Exception, *message, raise_exception: bool = True):
        self.logger(message=message, level=LOGGING_LEVEL['ERROR'])
        if not raise_exception: return None
        raise error(*message)


ELANGAI_WARNING = ElangAIWarning()
ELANGAI_INFO = ElangAIInfo()
ELANGAI_DEBUG = ElangAIDebug()
ELANGAI_CRITICAL = ElangAICritical()
ELANGAI_ERROR = ElangAIError()
