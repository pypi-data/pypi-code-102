# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Keras layers API.
"""

from __future__ import print_function as _print_function

import sys as _sys

from . import experimental
from tensorflow.python.keras.engine.base_layer import Layer
from tensorflow.python.keras.engine.base_layer_utils import disable_v2_dtype_behavior
from tensorflow.python.keras.engine.base_layer_utils import enable_v2_dtype_behavior
from tensorflow.python.keras.engine.input_layer import Input
from tensorflow.python.keras.engine.input_layer import InputLayer
from tensorflow.python.keras.engine.input_spec import InputSpec
from tensorflow.python.keras.feature_column.dense_features import DenseFeatures
from tensorflow.python.keras.layers.advanced_activations import ELU
from tensorflow.python.keras.layers.advanced_activations import LeakyReLU
from tensorflow.python.keras.layers.advanced_activations import PReLU
from tensorflow.python.keras.layers.advanced_activations import ReLU
from tensorflow.python.keras.layers.advanced_activations import Softmax
from tensorflow.python.keras.layers.advanced_activations import ThresholdedReLU
from tensorflow.python.keras.layers.convolutional import Conv1D
from tensorflow.python.keras.layers.convolutional import Conv1D as Convolution1D
from tensorflow.python.keras.layers.convolutional import Conv1DTranspose
from tensorflow.python.keras.layers.convolutional import Conv1DTranspose as Convolution1DTranspose
from tensorflow.python.keras.layers.convolutional import Conv2D
from tensorflow.python.keras.layers.convolutional import Conv2D as Convolution2D
from tensorflow.python.keras.layers.convolutional import Conv2DTranspose
from tensorflow.python.keras.layers.convolutional import Conv2DTranspose as Convolution2DTranspose
from tensorflow.python.keras.layers.convolutional import Conv3D
from tensorflow.python.keras.layers.convolutional import Conv3D as Convolution3D
from tensorflow.python.keras.layers.convolutional import Conv3DTranspose
from tensorflow.python.keras.layers.convolutional import Conv3DTranspose as Convolution3DTranspose
from tensorflow.python.keras.layers.convolutional import Cropping1D
from tensorflow.python.keras.layers.convolutional import Cropping2D
from tensorflow.python.keras.layers.convolutional import Cropping3D
from tensorflow.python.keras.layers.convolutional import DepthwiseConv2D
from tensorflow.python.keras.layers.convolutional import SeparableConv1D
from tensorflow.python.keras.layers.convolutional import SeparableConv1D as SeparableConvolution1D
from tensorflow.python.keras.layers.convolutional import SeparableConv2D
from tensorflow.python.keras.layers.convolutional import SeparableConv2D as SeparableConvolution2D
from tensorflow.python.keras.layers.convolutional import UpSampling1D
from tensorflow.python.keras.layers.convolutional import UpSampling2D
from tensorflow.python.keras.layers.convolutional import UpSampling3D
from tensorflow.python.keras.layers.convolutional import ZeroPadding1D
from tensorflow.python.keras.layers.convolutional import ZeroPadding2D
from tensorflow.python.keras.layers.convolutional import ZeroPadding3D
from tensorflow.python.keras.layers.convolutional_recurrent import ConvLSTM2D
from tensorflow.python.keras.layers.core import Activation
from tensorflow.python.keras.layers.core import ActivityRegularization
from tensorflow.python.keras.layers.core import Dense
from tensorflow.python.keras.layers.core import Dropout
from tensorflow.python.keras.layers.core import Flatten
from tensorflow.python.keras.layers.core import Lambda
from tensorflow.python.keras.layers.core import Masking
from tensorflow.python.keras.layers.core import Permute
from tensorflow.python.keras.layers.core import RepeatVector
from tensorflow.python.keras.layers.core import Reshape
from tensorflow.python.keras.layers.core import SpatialDropout1D
from tensorflow.python.keras.layers.core import SpatialDropout2D
from tensorflow.python.keras.layers.core import SpatialDropout3D
from tensorflow.python.keras.layers.cudnn_recurrent import CuDNNGRU
from tensorflow.python.keras.layers.cudnn_recurrent import CuDNNLSTM
from tensorflow.python.keras.layers.dense_attention import AdditiveAttention
from tensorflow.python.keras.layers.dense_attention import Attention
from tensorflow.python.keras.layers.embeddings import Embedding
from tensorflow.python.keras.layers.local import LocallyConnected1D
from tensorflow.python.keras.layers.local import LocallyConnected2D
from tensorflow.python.keras.layers.merge import Add
from tensorflow.python.keras.layers.merge import Average
from tensorflow.python.keras.layers.merge import Concatenate
from tensorflow.python.keras.layers.merge import Dot
from tensorflow.python.keras.layers.merge import Maximum
from tensorflow.python.keras.layers.merge import Minimum
from tensorflow.python.keras.layers.merge import Multiply
from tensorflow.python.keras.layers.merge import Subtract
from tensorflow.python.keras.layers.merge import add
from tensorflow.python.keras.layers.merge import average
from tensorflow.python.keras.layers.merge import concatenate
from tensorflow.python.keras.layers.merge import dot
from tensorflow.python.keras.layers.merge import maximum
from tensorflow.python.keras.layers.merge import minimum
from tensorflow.python.keras.layers.merge import multiply
from tensorflow.python.keras.layers.merge import subtract
from tensorflow.python.keras.layers.multi_head_attention import MultiHeadAttention
from tensorflow.python.keras.layers.noise import AlphaDropout
from tensorflow.python.keras.layers.noise import GaussianDropout
from tensorflow.python.keras.layers.noise import GaussianNoise
from tensorflow.python.keras.layers.normalization.batch_normalization_v1 import BatchNormalization
from tensorflow.python.keras.layers.normalization.layer_normalization import LayerNormalization
from tensorflow.python.keras.layers.pooling import AveragePooling1D
from tensorflow.python.keras.layers.pooling import AveragePooling1D as AvgPool1D
from tensorflow.python.keras.layers.pooling import AveragePooling2D
from tensorflow.python.keras.layers.pooling import AveragePooling2D as AvgPool2D
from tensorflow.python.keras.layers.pooling import AveragePooling3D
from tensorflow.python.keras.layers.pooling import AveragePooling3D as AvgPool3D
from tensorflow.python.keras.layers.pooling import GlobalAveragePooling1D
from tensorflow.python.keras.layers.pooling import GlobalAveragePooling1D as GlobalAvgPool1D
from tensorflow.python.keras.layers.pooling import GlobalAveragePooling2D
from tensorflow.python.keras.layers.pooling import GlobalAveragePooling2D as GlobalAvgPool2D
from tensorflow.python.keras.layers.pooling import GlobalAveragePooling3D
from tensorflow.python.keras.layers.pooling import GlobalAveragePooling3D as GlobalAvgPool3D
from tensorflow.python.keras.layers.pooling import GlobalMaxPooling1D
from tensorflow.python.keras.layers.pooling import GlobalMaxPooling1D as GlobalMaxPool1D
from tensorflow.python.keras.layers.pooling import GlobalMaxPooling2D
from tensorflow.python.keras.layers.pooling import GlobalMaxPooling2D as GlobalMaxPool2D
from tensorflow.python.keras.layers.pooling import GlobalMaxPooling3D
from tensorflow.python.keras.layers.pooling import GlobalMaxPooling3D as GlobalMaxPool3D
from tensorflow.python.keras.layers.pooling import MaxPooling1D
from tensorflow.python.keras.layers.pooling import MaxPooling1D as MaxPool1D
from tensorflow.python.keras.layers.pooling import MaxPooling2D
from tensorflow.python.keras.layers.pooling import MaxPooling2D as MaxPool2D
from tensorflow.python.keras.layers.pooling import MaxPooling3D
from tensorflow.python.keras.layers.pooling import MaxPooling3D as MaxPool3D
from tensorflow.python.keras.layers.recurrent import AbstractRNNCell
from tensorflow.python.keras.layers.recurrent import GRU
from tensorflow.python.keras.layers.recurrent import GRUCell
from tensorflow.python.keras.layers.recurrent import LSTM
from tensorflow.python.keras.layers.recurrent import LSTMCell
from tensorflow.python.keras.layers.recurrent import RNN
from tensorflow.python.keras.layers.recurrent import SimpleRNN
from tensorflow.python.keras.layers.recurrent import SimpleRNNCell
from tensorflow.python.keras.layers.recurrent import StackedRNNCells
from tensorflow.python.keras.layers.serialization import deserialize
from tensorflow.python.keras.layers.serialization import serialize
from tensorflow.python.keras.layers.wrappers import Bidirectional
from tensorflow.python.keras.layers.wrappers import TimeDistributed
from tensorflow.python.keras.layers.wrappers import Wrapper

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "keras.layers", public_apis=None, deprecation=True,
      has_lite=False)
