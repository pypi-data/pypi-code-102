import ssl
from typing import cast, Tuple

import sniffio
from httpcore import (
    AsyncConnectionPool,
    Origin,
    AsyncConnectionInterface,
    Request,
    Response,
    default_ssl_context,
    AsyncHTTP11Connection,
    ConnectionNotAvailable,
)
from httpcore.backends.base import AsyncNetworkStream

# noinspection PyProtectedMember
from httpcore._synchronization import AsyncLock

from python_socks import ProxyType, parse_proxy_url


class AsyncProxy(AsyncConnectionPool):
    def __init__(
        self,
        *,
        proxy_type: ProxyType,
        proxy_host: str,
        proxy_port: int,
        username=None,
        password=None,
        rdns=None,
        loop=None,
        **kwargs,
    ):
        self._proxy_type = proxy_type
        self._proxy_host = proxy_host
        self._proxy_port = proxy_port
        self._username = username
        self._password = password
        self._rdns = rdns
        self._loop = loop

        super().__init__(**kwargs)

    def create_connection(self, origin: Origin) -> AsyncConnectionInterface:
        return AsyncProxyConnection(
            proxy_type=self._proxy_type,
            proxy_host=self._proxy_host,
            proxy_port=self._proxy_port,
            username=self._username,
            password=self._password,
            rdns=self._rdns,
            loop=self._loop,
            remote_origin=origin,
            ssl_context=self._ssl_context,
            keepalive_expiry=self._keepalive_expiry,
            http1=self._http1,
            http2=self._http2,
        )

    @classmethod
    def from_url(cls, url, **kwargs):
        proxy_type, host, port, username, password = parse_proxy_url(url)
        return cls(
            proxy_type=proxy_type,
            proxy_host=host,
            proxy_port=port,
            username=username,
            password=password,
            **kwargs,
        )


class AsyncProxyConnection(AsyncConnectionInterface):
    def __init__(
        self,
        *,
        proxy_type: ProxyType,
        proxy_host: str,
        proxy_port: int,
        username=None,
        password=None,
        rdns=None,
        loop=None,
        # proxy_origin: Origin,
        remote_origin: Origin,
        ssl_context: ssl.SSLContext,
        keepalive_expiry: float = None,
        http1: bool = True,
        http2: bool = False,
    ) -> None:

        if ssl_context is None:  # pragma: no cover
            ssl_context = default_ssl_context()

        self._proxy_type = proxy_type
        self._proxy_host = proxy_host
        self._proxy_port = proxy_port
        self._username = username
        self._password = password
        self._rdns = rdns
        self._loop = loop

        self._remote_origin = remote_origin
        self._ssl_context = ssl_context
        self._keepalive_expiry = keepalive_expiry
        self._http1 = http1
        self._http2 = http2

        self._connect_lock = AsyncLock()
        self._connection = None

    async def handle_async_request(self, request: Request) -> Response:
        timeouts = request.extensions.get('timeout', {})
        timeout = timeouts.get('connect', None)

        async with self._connect_lock:
            if self._connection is None:
                stream = await self._connect_via_proxy(
                    origin=self._remote_origin,
                    connect_timeout=timeout,
                )

                ssl_object = stream.get_extra_info("ssl_object")
                http2_negotiated = (
                    ssl_object is not None and ssl_object.selected_alpn_protocol() == "h2"
                )
                if http2_negotiated or (self._http2 and not self._http1):  # pragma: no cover
                    from httpcore import AsyncHTTP2Connection

                    self._connection = AsyncHTTP2Connection(
                        origin=self._remote_origin,
                        stream=stream,
                        keepalive_expiry=self._keepalive_expiry,
                    )
                else:
                    self._connection = AsyncHTTP11Connection(
                        origin=self._remote_origin,
                        stream=stream,
                        keepalive_expiry=self._keepalive_expiry,
                    )
            elif not self._connection.is_available():  # pragma: no cover
                raise ConnectionNotAvailable()

            return await self._connection.handle_async_request(request)

    async def _connect_via_proxy(self, origin, connect_timeout) -> AsyncNetworkStream:
        scheme, hostname, port = origin.scheme, origin.host, origin.port

        ssl_context = self._ssl_context if scheme == b'https' else None
        host = hostname.decode('ascii')  # ?

        return await self._open_stream(
            host=host,
            port=port,
            connect_timeout=connect_timeout,
            ssl_context=ssl_context,
        )

    async def _open_stream(self, host, port, connect_timeout, ssl_context):
        backend = sniffio.current_async_library()

        if backend == 'asyncio':
            return await self._open_aio_stream(host, port, connect_timeout, ssl_context)

        if backend == 'trio':
            return await self._open_trio_stream(host, port, connect_timeout, ssl_context)

        # Curio support has been dropped in httpcore 0.14.0
        # if backend == 'curio':
        #     return await self._open_curio_stream(host, port, connect_timeout, ssl_context)

        raise RuntimeError(f'Unsupported concurrency backend {backend!r}')  # pragma: no cover

    async def _open_aio_stream(self, host, port, connect_timeout, ssl_context):
        import asyncio

        # noinspection PyProtectedMember
        from anyio._backends._asyncio import SocketStream, StreamProtocol
        from httpcore.backends.asyncio import AsyncIOStream
        from python_socks.async_.asyncio import Proxy

        if self._loop is None:
            self._loop = asyncio.get_event_loop()

        proxy = Proxy.create(
            loop=self._loop,
            proxy_type=self._proxy_type,
            host=self._proxy_host,
            port=self._proxy_port,
            username=self._username,
            password=self._password,
            rdns=self._rdns,
        )

        sock = await proxy.connect(host, port, timeout=connect_timeout)

        # see anyio._backends._asyncio connect_tcp
        transport, protocol = cast(
            Tuple[asyncio.Transport, StreamProtocol],
            await self._loop.create_connection(
                StreamProtocol,
                host=None,
                port=None,
                sock=sock,
            ),
        )
        transport.pause_reading()

        stream = AsyncIOStream(SocketStream(transport, protocol))
        if ssl_context is not None:
            stream = await stream.start_tls(
                ssl_context=ssl_context,
                server_hostname=host,
                timeout=connect_timeout,
            )
        return stream

    async def _open_trio_stream(self, host, port, connect_timeout, ssl_context):
        import trio
        from httpcore.backends.trio import TrioStream
        from python_socks.async_.trio import Proxy

        proxy = Proxy.create(
            proxy_type=self._proxy_type,
            host=self._proxy_host,
            port=self._proxy_port,
            username=self._username,
            password=self._password,
            rdns=self._rdns,
        )

        sock = await proxy.connect(host, port, timeout=connect_timeout)

        stream = TrioStream(trio.SocketStream(sock))

        if ssl_context is not None:
            stream = await stream.start_tls(
                ssl_context=ssl_context,
                server_hostname=host,
                timeout=connect_timeout,
            )

        return stream

    async def aclose(self) -> None:
        if self._connection is not None:
            await self._connection.aclose()

    def can_handle_request(self, origin: Origin) -> bool:
        return origin == self._remote_origin

    def is_available(self) -> bool:
        if self._connection is None:  # pragma: no cover
            # If HTTP/2 support is enabled, and the resulting connection could
            # end up as HTTP/2 then we should indicate the connection as being
            # available to service multiple requests.
            return self._http2 and (self._remote_origin.scheme == b"https" or not self._http1)
        return self._connection.is_available()

    def has_expired(self) -> bool:
        if self._connection is None:  # pragma: no cover
            return False
        return self._connection.has_expired()

    def is_idle(self) -> bool:
        if self._connection is None:  # pragma: no cover
            return False
        return self._connection.is_idle()

    def is_closed(self) -> bool:
        if self._connection is None:  # pragma: no cover
            return False
        return self._connection.is_closed()

    def info(self) -> str:
        if self._connection is None:  # pragma: no cover
            return "CONNECTING"
        return self._connection.info()
