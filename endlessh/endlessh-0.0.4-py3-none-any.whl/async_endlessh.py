import argparse
import asyncio
from logging import log
import random
import timeit
from time import time

import codefast as cf
from codefast.logger import Logger
logger = Logger(logname='/tmp/endlessh.log')
logger.level = 'INFO'

class Hosts:
    peer = {}


async def handler(_reader, writer):
    try:
        while True:
            await asyncio.sleep(3)
            peer = _reader._transport.get_extra_info('peername')
            if peer not in Hosts.peer:
                Hosts.peer[peer] = timeit.default_timer()
                logger.info('Connection from {}'.format(peer))
            writer.write(b'%x\r\n' % random.randint(0, 2**32))
            await writer.drain()
    except ConnectionResetError:
        logger.info('Connection closed by peer {} {:.1f} seconds '.format(
            peer,
            timeit.default_timer() - Hosts.peer[peer]))
        Hosts.peer.pop(peer)


async def main(port):
    server = await asyncio.start_server(handler, '0.0.0.0', port)
    async with server:
        await server.serve_forever()


def endlessh():
    parser = argparse.ArgumentParser(description='Run a fake ssh server')
    parser.add_argument("--port",
                        "-p",
                        help="The port to bind the ssh server to (default 22)",
                        default=22,
                        type=int,
                        action="store")
    args = parser.parse_args()
    asyncio.run(main(args.port))


endlessh()
