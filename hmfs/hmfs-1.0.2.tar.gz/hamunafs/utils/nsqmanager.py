
import traceback
from gnsq import Producer, Consumer, Message, NsqdHTTPClient
from aonsq import NSQMessage, NSQ
from hamunafs.utils.singleton_wrapper import Singleton

import asyncio

import copy

import orjson


class MQManager(Singleton):
    def __init__(self, host, port, async_mq=False):
        if async_mq:
            self.mq = NSQ(host, port)
        else:
            self.addr = '{}:{}'.format(host, port)
            self.producer = Producer(nsqd_tcp_addresses=[self.addr])
            self.producer.start()
            
    async def _init_async(self):
        await self.mq.connect()

    def publish(self, topic, message):
        try:
            if isinstance(message, str):
                message = message.encode('utf-8')
            else:
                message = orjson.dumps(message)
            ret = self.producer.publish(topic, message).decode()
        except Exception as e:
            print(traceback.print_exc())
            ret = False
        max_t = 5
        t = 0
        while ret != 'OK' and t < max_t: 
            try:
                ret = self.producer.publish(topic, message).decode()
            except:
                ret = 'ERR'
            t += 1
        return ret == 'OK'

    async def async_publish(self, topic, message):
        try:
            if isinstance(message, str):
                message = message.encode('utf-8')
            else:
                message = orjson.dumps(message)
            ret = await self.mq.pub(topic, message)
        except Exception as e:
            print(traceback.print_exc())
            ret = False
        max_t = 5
        t = 0
        while not ret and t < max_t: 
            try:
                ret = await self.mq.pub(topic, message)
            except:
                ret = False
            t += 1
        return ret

if __name__ == "__main__":
    manager = MQManager('kafka.ai.hamuna.club', 34150, async_mq=True)
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(manager._init_async())
    
    for i in range(100):
        ret = loop.run_until_complete(manager.async_publish('test', 'test'))
        # ret = manager.publish('test', 'test'.encode('utf-8'))
        print(ret)