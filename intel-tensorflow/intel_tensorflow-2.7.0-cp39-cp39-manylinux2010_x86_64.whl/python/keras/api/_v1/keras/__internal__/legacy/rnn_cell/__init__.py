# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Public API for tf.keras.__internal__.legacy.rnn_cell namespace.
"""

from __future__ import print_function as _print_function

import sys as _sys

from tensorflow.python.keras.layers.legacy_rnn.rnn_cell_impl import BasicLSTMCell
from tensorflow.python.keras.layers.legacy_rnn.rnn_cell_impl import BasicRNNCell
from tensorflow.python.keras.layers.legacy_rnn.rnn_cell_impl import DeviceWrapper
from tensorflow.python.keras.layers.legacy_rnn.rnn_cell_impl import DropoutWrapper
from tensorflow.python.keras.layers.legacy_rnn.rnn_cell_impl import GRUCell
from tensorflow.python.keras.layers.legacy_rnn.rnn_cell_impl import LSTMCell
from tensorflow.python.keras.layers.legacy_rnn.rnn_cell_impl import LSTMStateTuple
from tensorflow.python.keras.layers.legacy_rnn.rnn_cell_impl import MultiRNNCell
from tensorflow.python.keras.layers.legacy_rnn.rnn_cell_impl import RNNCell
from tensorflow.python.keras.layers.legacy_rnn.rnn_cell_impl import ResidualWrapper

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "keras.__internal__.legacy.rnn_cell", public_apis=None, deprecation=True,
      has_lite=False)
