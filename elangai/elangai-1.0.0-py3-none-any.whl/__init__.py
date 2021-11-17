# Copyright 2021 elangai Developer. All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
#
# Written by Resha Al-Fahsi <resha.alfahsi@techbros.io>, 2021.
# =========================================================================


from elangai.__about__ import __version__
import sys


__python_version__ = sys.version_info


if __python_version__ < (3,6):
    raise Exception('Your Python version: ' + \
                    str(__python_version__.major) + '.' + \
                    str(__python_version__.minor) + '.' + \
                    str(__python_version__.micro) + ' is not supported')


del __python_version__


from .callback import *
from .interface import *
from .utils import *

from .model import ElangChainer
from .inference import ElangInference
