from email import header
from pydoc import cli
from diskcache import Cache
from threading import Lock

from hamunafs.utils.redisutil import XRedis
from hamunafs.utils.nsqmanager import MQManager
from hamunafs.backends import BackendBase, backend_factory


import random
import os
import shutil
import time
import uuid
import json
import httpx

class Client:
    @staticmethod
    def get_client(host, redis_client: XRedis, mq_manager: MQManager, async_mq_mode=True, cache_path='../cache'):
        client = Client(host, redis_client, mq_manager, async_mq_mode)
        return client
    
    def __init__(self, host, redis_client: XRedis, mq_manager: MQManager, async_mq_mode=True, cache_path='../cache') -> None:
        self.host = host
        self.redis = redis_client
        self.mq = mq_manager
        self.async_mq = async_mq_mode
        self.lock = Lock()
        
        #self.cache_path = cache_path
        os.makedirs(cache_path, exist_ok=True)
        self.index_cache = Cache(cache_path)
        
        self.put_topic = 'fs_put'
        self.get_topic = 'fs_get'
        
        self.update()
    
    def update(self):
        with self.lock:
            print('updating backends...')
            resp = httpx.get('https://{}/api/system/fs/backends'.format(self.host), headers={
                'from': 'edge'
            })
            if resp.status_code == 200:
                resp = json.loads(resp.text)
                if resp['success'] == 'ok':
                    backend_pools = {}
                    pool_data = resp['data']
                    for info in pool_data:
                        backend_pools[info['key']] = backend_factory[info['backend']](info['conf'])
                        self.backend_pools = backend_pools
                else:
                    raise Exception('error on acquiring fs backends...')
            else:
                raise Exception('error on acquiring fs backends...')
        
    def _random_pick_backend(self) -> BackendBase:
        with self.lock:
            keys = list(self.backend_pools.keys())
            
            selected_key = random.sample(keys, 1)[0]
            return selected_key, self.backend_pools[selected_key]
    
    def _get_appropriate_backend(self, url):
        with self.lock:
            prefix, _url = url.split('://')
            
            if prefix in self.backend_pools:
                bucket, bucket_name = _url.split('/')        
                return self.backend_pools[prefix], bucket, bucket_name
            return None, None, None

    def cache(self, key, val, ttl=7200):
        if not isinstance(val, str):
            _val = json.dumps(val)
        else:
            _val = val
        try:
            with self.redis._get_connection(pipeline=True) as pipe:
                pipe.set(key, _val)
                pipe.set_expire_time(key, ttl)
                pipe.execute()
        except:
            pass
        self.index_cache.set(key, _val, expire=ttl)

    def get_cache(self, key, toObj=True):
        data = self.index_cache.get(key)
        if data is None:
            data = self.redis.get(key)

        if data is not None and toObj:
            data = json.loads(data)
        
        return data
            
    def put_to_cloud(self, path, bucket, bucket_name, tmp=True):
        cache_key = 'cloud_{}_{}'.format(bucket, bucket_name)
        cache_data = self.get_cache(cache_key, toObj=False)
        if cache_data is None:
            prefix, backend = self._random_pick_backend()
            
            ret, e = backend.put(path, bucket, bucket_name, tmp)
            if ret:
                url = '{}://{}'.format(prefix, e)
                self.cache(cache_key, url)
                return True, url
            return ret, e
        else:
            return True, cache_data
    
    def get_from_cloud(self, path, url, force_copy=False, min_size=0):
        file_path = self.index_cache.get(url)
        if file_path is not None and os.path.isfile(file_path) and os.path.getsize(file_path) // 1024 >= min_size:
            print('loading from disk...')
            if force_copy:
                if file_path == path:
                    return True, path
                else:
                    os.makedirs(os.path.split(path)[0], exist_ok=True)
                    
                    shutil.copy(file_path, path)
                    
                    return True, path
            return True, file_path             
        
        print('loading from cloud...')
        backend, bucket, bucket_name = self._get_appropriate_backend(url)
        
        if backend is not None:
            ret, e = backend.get(path, bucket, bucket_name)
            if ret:
                self.index_cache.set(url, e)
                return True, path
            else:
                return ret, e
        else:
            return False, '未受支持的Backend'
    
    def put(self, path, bucket, bucket_name, timeout=10, file_ttl=-1):
        ret, e = self.put_to_cloud(path, bucket, bucket_name)
        if ret:
            # save to cache
            task_id = 'tmp_file_{}_{}'.format(bucket, bucket_name)
            ret = self.mq.publish(self.put_topic, {
                'url': e,
                'bucket': bucket,
                'bucket_name': bucket_name,
                'ttl': file_ttl
            })
            
            if ret:
                t = time.time()
                while True:
                    if time.time() - t >= timeout:
                        break
                    
                    resp = self.redis.get(task_id)
                    
                    if resp is not None and len(resp) > 0:
                        resp = json.loads(resp)
                        if resp['ret']:
                            return True, '{}/{}'.format(bucket, bucket_name)
                        else:
                            return False, resp['err']
                    
                    time.sleep(1)
                
        return False, e
    
    def get(self, path, url, force_copy=False, min_size=0, timeout=10):
        if '://' in url:
            ret, e = self.get_from_cloud(path, url, force_copy, min_size)
            return ret, e
        
        bucket, bucket_name = url.split('/')
        task_id = 'tmp_file_{}_{}'.format(bucket, bucket_name)
        
        ret = self.mq.publish(self.get_topic, {
            'bucket': bucket,
            'bucket_name': bucket_name
        })
        if ret:
            t = time.time()
            resp = None
            while True:
                if time.time() - t >= timeout:
                    break
                
                resp = self.redis.get(task_id)
                if resp is not None and len(resp) > 0:
                    resp = json.loads(resp)
                    if resp['ret']:
                        tmp_url = resp['url']
                        return self.get_from_cloud(path, tmp_url, force_copy, min_size)
                
                time.sleep(1)
                
        return False, '获取失败'
                    
                    