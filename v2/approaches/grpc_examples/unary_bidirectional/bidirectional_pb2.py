# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bidirectional.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13\x62idirectional.proto\x12\rbidirectional\"\x1a\n\x07Message\x12\x0f\n\x07message\x18\x01 \x01(\t2Z\n\rBidirectional\x12I\n\x11GetServerResponse\x12\x16.bidirectional.Message\x1a\x16.bidirectional.Message\"\x00(\x01\x30\x01\x62\x06proto3')



_MESSAGE = DESCRIPTOR.message_types_by_name['Message']
Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), {
  'DESCRIPTOR' : _MESSAGE,
  '__module__' : 'bidirectional_pb2'
  # @@protoc_insertion_point(class_scope:bidirectional.Message)
  })
_sym_db.RegisterMessage(Message)

_BIDIRECTIONAL = DESCRIPTOR.services_by_name['Bidirectional']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MESSAGE._serialized_start=38
  _MESSAGE._serialized_end=64
  _BIDIRECTIONAL._serialized_start=66
  _BIDIRECTIONAL._serialized_end=156
# @@protoc_insertion_point(module_scope)