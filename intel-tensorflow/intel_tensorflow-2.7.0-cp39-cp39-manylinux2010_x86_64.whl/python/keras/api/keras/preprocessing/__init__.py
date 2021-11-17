# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Provides keras data preprocessing utils to pre-process tf.data.Datasets before they are fed to the model.
"""

from __future__ import print_function as _print_function

import sys as _sys

from . import image
from . import sequence
from . import text

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "keras.preprocessing", public_apis=None, deprecation=True,
      has_lite=False)
