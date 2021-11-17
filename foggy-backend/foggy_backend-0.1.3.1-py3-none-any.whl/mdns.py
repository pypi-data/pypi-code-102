"""Module to configure the zeroconf multicast dns service broadcast."""
import logging
from contextlib import contextmanager
import socket

from zeroconf import ServiceInfo, Zeroconf, IPVersion

logging.getLogger(__name__).addHandler(logging.NullHandler())


SERVICEINFO = ServiceInfo(
    "_foggy._tcp.local.",
    "Arne._foggy._tcp.local.",
    server=socket.gethostname(),
    addresses=[socket.inet_aton("127.0.0.1")],
    port=21210,
    # properties=desc,
)


@contextmanager
def broadcast_service():
    try:
        logging.info("Starting service broadcast")
        zeroconf = Zeroconf(ip_version=IPVersion.V4Only)
        zeroconf.register_service(SERVICEINFO)
        yield
    finally:
        logging.info("Stopping service broadcast")
        zeroconf.unregister_service(SERVICEINFO)
        zeroconf.close()
