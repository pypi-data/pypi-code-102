# Copyright 2021 elangai Developer. All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
#
# Written by Resha Al-Fahsi <resha.alfahsi@techbros.io>, 2021.
# =========================================================================


from elangai.logger._core import CoreLogger


class Logger:
    def __valid_logger__(self, **kwargs):
        return True if 'message' in kwargs and 'level' in kwargs else False
           
    def __call__(self, **kwargs):
        assert self.__valid_logger__(**kwargs), "logger must have message and level arguments"
        CoreLogger.scream(kwargs['message'], kwargs['level'])
    

def elangai_logger(cls):
    logger = Logger()
    setattr(cls, 'logger', logger)
    return cls
