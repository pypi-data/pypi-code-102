"""Caching retrieved information"""

from os.path import isfile
import pickle
from .api import get_vinfo, get_chinfo


class YT_Info_Cache_Base(object):

    def __init__(self, path, downloader):
        assert isfile(path)
        self.path = path
        self._load(path)
        
        assert callable(downloader)
        self.downloader = downloader


    def _load(self, path):
        with open(path, "rb") as f:
            self.dict = pickle.load(f)


    def get(self, obj_id, part, v=False):

        info = self.dict.get(obj_id)
        names = part.strip().split(',')

        need_download = False
        if info is None:
            need_download = True
            info = {}
        elif info == {}:
            need_download = False
            if v: print("The information for id='{}' might not be available".format(obj_id))
        else:
            if any((name not in info.keys() for name in names)):
                need_download = True
            else:
                if v: print("Found information for id='{}' from cache".format(obj_id))

        if need_download:
            if v: print("Retrieving information for id='{}' from server ... ".format(obj_id), end='')
            res = self.downloader(obj_id, part=part)
            if len(res) == 0:
                if v: print("not found")
                info = {}
            else:
                info_retrieved, = res
                for name in names:
                    if name not in info_retrieved:
                        info_retrieved[name] = {}
                if v: print("found")
                info.update(info_retrieved)

        self.dict.update({obj_id:info})

        return info


    def save(self):
        with open(self.path, 'wb') as f:
            pickle.dump(self.dict, f, protocol=pickle.HIGHEST_PROTOCOL)





class YT_Video_Info_Cache(YT_Info_Cache_Base):

    def __init__(self, path):
        super().__init__(path, get_vinfo)
    
    def get_chid(self, vid, v=False):
        chid = None
        vinfo = self.get(vid, part='snippet', v=v)
        if vinfo is None:
            if v: print("No information for vid='{}'".format(vid))
        elif vinfo == {}:
            if v: print("Video for vid='{}' might have been deleted".format(vid))
        else:
            snippet = vinfo.get('snippet')
            if snippet is None:
                raise Exception("Unexpected case for vid='{}'".format(vid))
            else: chid = snippet['channelId']
        return chid




class YT_Channel_Info_Cache(YT_Info_Cache_Base):
    def __init__(self, path):
        super().__init__(path, get_chinfo)


