# Copyright 2021 elangai Developer. All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
#
# Written by Resha Al-Fahsi <resha.alfahsi@techbros.io>, 2021.
# =========================================================================


import time

from functools import wraps
from elangai.utils._logging import ELANGAI_INFO, ELANGAI_ERROR


def fps_counter(func):
    """Wrapper to check the fps of the inference function.

    :param func: inference function
    :return: wrapper function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        ret = func(*args, **kwargs)
        end = time.perf_counter()
        fps = 1./(end - start)
        return ret, fps
    return wrapper


def elang_timer(func):
    """Wrapper to measure elapsed time required 
       to execute the test function.

    :param func: test function
    :return: wrapper function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        ret = func(*args, **kwargs)
        end = time.perf_counter()
        ELANGAI_INFO("Finished in {}s".format(end-start))
        return ret
    return wrapper
