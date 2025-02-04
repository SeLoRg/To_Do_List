# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: auth.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'auth.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nauth.proto\x12\x04\x61uth\x1a\x1egoogle/protobuf/wrappers.proto\"\x1e\n\x0b\x43redentials\x12\x0f\n\x07user_id\x18\x01 \x01(\t\"5\n\x06Tokens\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x01 \x01(\t\x12\x15\n\rrefresh_token\x18\x02 \x01(\t\"K\n\x10\x43heckAuthRequest\x12\n\n\x02ip\x18\x01 \x01(\t\x12\r\n\x05\x61gent\x18\x02 \x01(\t\x12\x1c\n\x06tokens\x18\x03 \x01(\x0b\x32\x0c.auth.Tokens\"\x98\x01\n\x11\x43heckAuthResponse\x12\x10\n\x08is_login\x18\x01 \x01(\x08\x12%\n\nnew_tokens\x18\x02 \x01(\x0b\x32\x0c.auth.TokensH\x00\x88\x01\x01\x12+\n\x0b\x63redentials\x18\x04 \x01(\x0b\x32\x11.auth.CredentialsH\x01\x88\x01\x01\x42\r\n\x0b_new_tokensB\x0e\n\x0c_credentials\"O\n\x0cLoginRequest\x12\n\n\x02ip\x18\x01 \x01(\t\x12\r\n\x05\x61gent\x18\x02 \x01(\t\x12\x12\n\nuser_email\x18\x03 \x01(\t\x12\x10\n\x08password\x18\x04 \x01(\t\"O\n\rLoginResponse\x12\x10\n\x08is_login\x18\x01 \x01(\x08\x12!\n\x06tokens\x18\x02 \x01(\x0b\x32\x0c.auth.TokensH\x00\x88\x01\x01\x42\t\n\x07_tokens\"7\n\rLogoutRequest\x12&\n\x0b\x63redentials\x18\x01 \x01(\x0b\x32\x11.auth.Credentials\"#\n\x0eLogoutResponse\x12\x11\n\tis_logout\x18\x01 \x01(\x08\x32\xb2\x01\n\x0b\x41uthService\x12<\n\tCheckAuth\x12\x16.auth.CheckAuthRequest\x1a\x17.auth.CheckAuthResponse\x12\x30\n\x05Login\x12\x12.auth.LoginRequest\x1a\x13.auth.LoginResponse\x12\x33\n\x06Logout\x12\x13.auth.LogoutRequest\x1a\x14.auth.LogoutResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'auth_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CREDENTIALS']._serialized_start=52
  _globals['_CREDENTIALS']._serialized_end=82
  _globals['_TOKENS']._serialized_start=84
  _globals['_TOKENS']._serialized_end=137
  _globals['_CHECKAUTHREQUEST']._serialized_start=139
  _globals['_CHECKAUTHREQUEST']._serialized_end=214
  _globals['_CHECKAUTHRESPONSE']._serialized_start=217
  _globals['_CHECKAUTHRESPONSE']._serialized_end=369
  _globals['_LOGINREQUEST']._serialized_start=371
  _globals['_LOGINREQUEST']._serialized_end=450
  _globals['_LOGINRESPONSE']._serialized_start=452
  _globals['_LOGINRESPONSE']._serialized_end=531
  _globals['_LOGOUTREQUEST']._serialized_start=533
  _globals['_LOGOUTREQUEST']._serialized_end=588
  _globals['_LOGOUTRESPONSE']._serialized_start=590
  _globals['_LOGOUTRESPONSE']._serialized_end=625
  _globals['_AUTHSERVICE']._serialized_start=628
  _globals['_AUTHSERVICE']._serialized_end=806
# @@protoc_insertion_point(module_scope)
