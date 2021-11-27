import argparse
import asyncio
import random
import timeit
from logging import log
from time import time

import codefast as cf
from codefast.logger import Logger

logger = Logger(logname='/tmp/endlessh.log')
logger.level = 'INFO'


class Hosts:
    peer = {}

    @classmethod
    def sort_by_time(cls):
        return sorted(cls.peer.items(), key=lambda p: p[1])


async def handler(_reader, writer):
    try:
        while True:
            await asyncio.sleep(3)
            peer = ':'.join(
                map(str, _reader._transport.get_extra_info('peername')))
            if peer not in Hosts.peer:
                Hosts.peer[peer] = timeit.default_timer()
                logger.info('connection from peer {}'.format(peer))
            writer.write(b'%x\r\n' % random.randint(0, 2**32))
            await writer.drain()
    except ConnectionResetError:
        logger.info(
            'connection closed by peer {} {:.1f} after seconds '.format(
                peer,
                timeit.default_timer() - Hosts.peer[peer]))
        Hosts.peer.pop(peer)
        logger.info('peers connected: 【 {} 】🦧'.format(len(Hosts.peer)))
        if Hosts.peer:
            list_ = Hosts.sort_by_time()
            host_id, host_time = list_[0]
            time_diff = round(timeit.default_timer() - host_time, 1)
            logger.info('most patient peer: {}, {} seconds 🐢'.format(
                host_id, time_diff))


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
