import socket
import getpass

from . import defines
from . import errors
from .opentelemetry import OpenTelemetryTraceContext
from .varint import write_varint
from .writer import write_binary_str, write_binary_uint8, \
    write_binary_uint64, write_binary_uint128


class ClientInfo(object):
    class Interface(object):
        TCP = 1
        HTTP = 2

    class QueryKind(object):
        # Uninitialized object.
        NO_QUERY = 0

        INITIAL_QUERY = 1

        # Query that was initiated by another query for distributed query
        # execution.
        SECONDARY_QUERY = 2

    client_version_major = defines.CLIENT_VERSION_MAJOR
    client_version_minor = defines.CLIENT_VERSION_MINOR
    client_version_patch = defines.CLIENT_VERSION_PATCH
    client_revision = defines.CLIENT_REVISION
    interface = Interface.TCP

    initial_user = ''
    initial_query_id = ''
    initial_address = '0.0.0.0:0'

    quota_key = ''

    def __init__(self, client_name, context):
        self.query_kind = ClientInfo.QueryKind.NO_QUERY

        try:
            self.os_user = getpass.getuser()
        except KeyError:
            self.os_user = ''
        self.client_hostname = socket.gethostname()
        self.client_name = client_name

        self.client_trace_context = OpenTelemetryTraceContext(
            context.client_settings['opentelemetry_traceparent'],
            context.client_settings['opentelemetry_tracestate']
        )

        super(ClientInfo, self).__init__()

    @property
    def empty(self):
        return self.query_kind == ClientInfo.QueryKind.NO_QUERY

    def write(self, server_revision, fout):
        revision = server_revision
        if server_revision < defines.DBMS_MIN_REVISION_WITH_CLIENT_INFO:
            raise errors.LogicalError('Method ClientInfo.write is called '
                                      'for unsupported server revision')

        write_binary_uint8(self.query_kind, fout)
        if self.empty:
            return

        write_binary_str(self.initial_user, fout)
        write_binary_str(self.initial_query_id, fout)
        write_binary_str(self.initial_address, fout)

        write_binary_uint8(self.interface, fout)

        write_binary_str(self.os_user, fout)
        write_binary_str(self.client_hostname, fout)
        write_binary_str(self.client_name, fout)
        write_varint(self.client_version_major, fout)
        write_varint(self.client_version_minor, fout)
        write_varint(self.client_revision, fout)

        if revision >= defines.DBMS_MIN_REVISION_WITH_QUOTA_KEY_IN_CLIENT_INFO:
            write_binary_str(self.quota_key, fout)

        if revision >= defines.DBMS_MIN_REVISION_WITH_VERSION_PATCH:
            write_varint(self.client_version_patch, fout)

        if revision >= defines.DBMS_MIN_REVISION_WITH_OPENTELEMETRY:
            if self.client_trace_context.trace_id is not None:
                # Have OpenTelemetry header.
                write_binary_uint8(1, fout)
                write_binary_uint128(self.client_trace_context.trace_id, fout)
                write_binary_uint64(self.client_trace_context.span_id, fout)
                write_binary_str(self.client_trace_context.tracestate, fout)
                write_binary_uint8(self.client_trace_context.trace_flags, fout)
            else:
                # Don't have OpenTelemetry header.
                write_binary_uint8(0, fout)
