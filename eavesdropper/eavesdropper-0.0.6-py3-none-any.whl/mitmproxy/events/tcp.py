"""TCP-specific events."""
from eavesdropper.mitmproxy import tcp
from . import GenericEvents


class Events(GenericEvents):
    def tcp_start(self, flow: tcp.TCPFlow):
        """
            A TCP connection has started.
        """

    def tcp_message(self, flow: tcp.TCPFlow):
        """
            A TCP connection has received a message. The most recent message
            will be flow.messages[-1]. The message is user-modifiable.
        """

    def tcp_error(self, flow: tcp.TCPFlow):
        """
            A TCP error has occurred.
        """

    def tcp_end(self, flow: tcp.TCPFlow):
        """
            A TCP connection has ended.
        """
