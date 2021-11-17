# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorflow/core/protobuf/tensor_bundle.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tensorflow.core.framework import tensor_shape_pb2 as tensorflow_dot_core_dot_framework_dot_tensor__shape__pb2
from tensorflow.core.framework import tensor_slice_pb2 as tensorflow_dot_core_dot_framework_dot_tensor__slice__pb2
from tensorflow.core.framework import types_pb2 as tensorflow_dot_core_dot_framework_dot_types__pb2
from tensorflow.core.framework import versions_pb2 as tensorflow_dot_core_dot_framework_dot_versions__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='tensorflow/core/protobuf/tensor_bundle.proto',
  package='tensorflow',
  syntax='proto3',
  serialized_options=_b('\n\023org.tensorflow.utilB\022TensorBundleProtosP\001ZUgithub.com/tensorflow/tensorflow/tensorflow/go/core/protobuf/for_core_protos_go_proto\370\001\001'),
  serialized_pb=_b('\n,tensorflow/core/protobuf/tensor_bundle.proto\x12\ntensorflow\x1a,tensorflow/core/framework/tensor_shape.proto\x1a,tensorflow/core/framework/tensor_slice.proto\x1a%tensorflow/core/framework/types.proto\x1a(tensorflow/core/framework/versions.proto\"\xb1\x01\n\x11\x42undleHeaderProto\x12\x12\n\nnum_shards\x18\x01 \x01(\x05\x12<\n\nendianness\x18\x02 \x01(\x0e\x32(.tensorflow.BundleHeaderProto.Endianness\x12\'\n\x07version\x18\x03 \x01(\x0b\x32\x16.tensorflow.VersionDef\"!\n\nEndianness\x12\n\n\x06LITTLE\x10\x00\x12\x07\n\x03\x42IG\x10\x01\"\xd2\x01\n\x10\x42undleEntryProto\x12#\n\x05\x64type\x18\x01 \x01(\x0e\x32\x14.tensorflow.DataType\x12+\n\x05shape\x18\x02 \x01(\x0b\x32\x1c.tensorflow.TensorShapeProto\x12\x10\n\x08shard_id\x18\x03 \x01(\x05\x12\x0e\n\x06offset\x18\x04 \x01(\x03\x12\x0c\n\x04size\x18\x05 \x01(\x03\x12\x0e\n\x06\x63rc32c\x18\x06 \x01(\x07\x12,\n\x06slices\x18\x07 \x03(\x0b\x32\x1c.tensorflow.TensorSliceProtoB\x85\x01\n\x13org.tensorflow.utilB\x12TensorBundleProtosP\x01ZUgithub.com/tensorflow/tensorflow/tensorflow/go/core/protobuf/for_core_protos_go_proto\xf8\x01\x01\x62\x06proto3')
  ,
  dependencies=[tensorflow_dot_core_dot_framework_dot_tensor__shape__pb2.DESCRIPTOR,tensorflow_dot_core_dot_framework_dot_tensor__slice__pb2.DESCRIPTOR,tensorflow_dot_core_dot_framework_dot_types__pb2.DESCRIPTOR,tensorflow_dot_core_dot_framework_dot_versions__pb2.DESCRIPTOR,])



_BUNDLEHEADERPROTO_ENDIANNESS = _descriptor.EnumDescriptor(
  name='Endianness',
  full_name='tensorflow.BundleHeaderProto.Endianness',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='LITTLE', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BIG', index=1, number=1,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=378,
  serialized_end=411,
)
_sym_db.RegisterEnumDescriptor(_BUNDLEHEADERPROTO_ENDIANNESS)


_BUNDLEHEADERPROTO = _descriptor.Descriptor(
  name='BundleHeaderProto',
  full_name='tensorflow.BundleHeaderProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='num_shards', full_name='tensorflow.BundleHeaderProto.num_shards', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='endianness', full_name='tensorflow.BundleHeaderProto.endianness', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='version', full_name='tensorflow.BundleHeaderProto.version', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _BUNDLEHEADERPROTO_ENDIANNESS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=234,
  serialized_end=411,
)


_BUNDLEENTRYPROTO = _descriptor.Descriptor(
  name='BundleEntryProto',
  full_name='tensorflow.BundleEntryProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='dtype', full_name='tensorflow.BundleEntryProto.dtype', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='shape', full_name='tensorflow.BundleEntryProto.shape', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='shard_id', full_name='tensorflow.BundleEntryProto.shard_id', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='offset', full_name='tensorflow.BundleEntryProto.offset', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='size', full_name='tensorflow.BundleEntryProto.size', index=4,
      number=5, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='crc32c', full_name='tensorflow.BundleEntryProto.crc32c', index=5,
      number=6, type=7, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='slices', full_name='tensorflow.BundleEntryProto.slices', index=6,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=414,
  serialized_end=624,
)

_BUNDLEHEADERPROTO.fields_by_name['endianness'].enum_type = _BUNDLEHEADERPROTO_ENDIANNESS
_BUNDLEHEADERPROTO.fields_by_name['version'].message_type = tensorflow_dot_core_dot_framework_dot_versions__pb2._VERSIONDEF
_BUNDLEHEADERPROTO_ENDIANNESS.containing_type = _BUNDLEHEADERPROTO
_BUNDLEENTRYPROTO.fields_by_name['dtype'].enum_type = tensorflow_dot_core_dot_framework_dot_types__pb2._DATATYPE
_BUNDLEENTRYPROTO.fields_by_name['shape'].message_type = tensorflow_dot_core_dot_framework_dot_tensor__shape__pb2._TENSORSHAPEPROTO
_BUNDLEENTRYPROTO.fields_by_name['slices'].message_type = tensorflow_dot_core_dot_framework_dot_tensor__slice__pb2._TENSORSLICEPROTO
DESCRIPTOR.message_types_by_name['BundleHeaderProto'] = _BUNDLEHEADERPROTO
DESCRIPTOR.message_types_by_name['BundleEntryProto'] = _BUNDLEENTRYPROTO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BundleHeaderProto = _reflection.GeneratedProtocolMessageType('BundleHeaderProto', (_message.Message,), {
  'DESCRIPTOR' : _BUNDLEHEADERPROTO,
  '__module__' : 'tensorflow.core.protobuf.tensor_bundle_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.BundleHeaderProto)
  })
_sym_db.RegisterMessage(BundleHeaderProto)

BundleEntryProto = _reflection.GeneratedProtocolMessageType('BundleEntryProto', (_message.Message,), {
  'DESCRIPTOR' : _BUNDLEENTRYPROTO,
  '__module__' : 'tensorflow.core.protobuf.tensor_bundle_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.BundleEntryProto)
  })
_sym_db.RegisterMessage(BundleEntryProto)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
