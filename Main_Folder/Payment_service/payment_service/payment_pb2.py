# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: payment.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rpayment.proto\"x\n\x0ePaymentMessage\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x10\n\x08order_id\x18\x02 \x01(\x05\x12\x0f\n\x07user_id\x18\x03 \x01(\x05\x12\x14\n\x0ctotal_amount\x18\x04 \x01(\x02\x12\x0e\n\x06status\x18\x05 \x01(\t\x12\x11\n\ttimestamp\x18\x06 \x01(\tb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'payment_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _PAYMENTMESSAGE._serialized_start=17
  _PAYMENTMESSAGE._serialized_end=137
# @@protoc_insertion_point(module_scope)
