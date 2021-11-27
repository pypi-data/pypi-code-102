"""For accessing Kizuna Ai gallary"""

from os.path import isdir, isfile, join
from operator import xor
from os import listdir
from sys import stderr
from datetime import datetime
import re

import numpy as np
from bs4 import BeautifulSoup


base_urls = {
    'lists':"https://gall.dcinside.com/mgallery/board/lists",
    'board':"https://gall.dcinside.com/mgallery/board/view",
}

user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
              ' AppleWebKit/537.36 (KHTML, like Gecko)'
              ' Chrome/94.0.4606.61 Safari/537.36')

header = {'User-Agent':user_agent}

gall_id = "kizunaai"


class Archive(object):
    
    fname_contents_form = 'view_content_wrap-N-{}-from-{}.bytes'
    
    def __init__(self, dpath):
        if not isdir(dpath):
            raise Exception("Directory not found : '{}'".format(dpath))
        self.dpath = dpath
        
    def load(self, post_no_srt_list, N_list, verbose=False):
        assert len(post_no_srt_list) == len(N_list)
        view_content_wrap_list = []
        for jj, post_no_srt in enumerate(post_no_srt_list):
            N = N_list[jj]
            fname_contents = self.fname_contents_form.format(N, post_no_srt)
            fpath_contents = join(self.dpath, fname_contents)
            assert isfile(fpath_contents)
            
            if verbose:
                print("Processing '{}' ... ".format(fpath_contents), end='')
            
            with open(fpath_contents, "rb") as f:
                contents = f.read()
                
            soup = BeautifulSoup(contents, 'html.parser')
            view_content_wrap_list_now = soup.find_all('div', {'class':'view_content_wrap'})
            view_content_wrap_list += view_content_wrap_list_now
            
            if verbose:
                print('done')
                
        return view_content_wrap_list





class ArrayArchive(object):
    
    _dname_form = "view_content_wrap-N-([0-9]+)-from-([0-9]+).npy"
    _index_fname = 'index.npy'
    _post_no_srt_name = 'post_no_srt'
    
    def __init__(self, dpath):
        
        #### Get arguments and set as members
        if not isdir(dpath): 
            raise Exception("Directory not found: '{}'".format(dpath))
        self.dpath = dpath
        
        #### Construct data information array
        data_file_info_arr = self._construct_info_arr(self.dpath)
        self._check_overlap(data_file_info_arr)
        self.data = data_file_info_arr
        
        #### Set index
        self._set_index(self.dpath, self.data)
        
        
    def _construct_info_arr(self, dpath):
        
        #### Construct array of data files and their information
        path_str_len_max = 0
        data_file_info_list = []
        patt = re.compile(self.__class__._dname_form)
        for name in listdir(dpath):
            path = join(self.dpath, name)
            if not isfile(path): continue
            
            N, post_no_srt = None, None
            res = re.search(patt, name)
            if res is None: continue
            else:
                extracted = res.groups()
                if len(extracted) != 2:
                    print("Strange data file found: '{}'".format(path), file=stderr)
                else:
                    N, post_no_srt = (int(s) for s in extracted)
            assert (N is not None) and (post_no_srt is not None)
            data_file_info = (path, post_no_srt, N)
            data_file_info_list.append(data_file_info)
            path_str_len_max = max(path_str_len_max, len(path))
        
        data_file_info_arr = np.array(data_file_info_list, dtype=[
            ('path',np.dtype(('U',path_str_len_max))),
            (self.__class__._post_no_srt_name,'i4'),
            ('N','i4')
        ])
        
        return data_file_info_arr
        
        
    def _check_overlap(self, data_file_info_arr):
        
        #### Check if there is any overlap among ranges of post numbers
        post_no_srt_name = self.__class__._post_no_srt_name
        data_file_info_arr.sort(order=post_no_srt_name)
        overlap_mask = data_file_info_arr[post_no_srt_name][1:] \
            < (data_file_info_arr[post_no_srt_name][:-1] + data_file_info_arr['N'][:-1])
        has_overlap = np.any(overlap_mask)
        if has_overlap:
            overlap_indices, = np.nonzero(overlap_mask)
            for j_overlap in overlap_indices:
                print(data_file_info_arr[j_overlap:j_overlap+2], file=stderr)
            raise Exception("There exists an overlap")
            

    
    def _set_index(self, dpath, data_file_info_arr):
    
        #### Update datetime index and check sync.
        index_fpath = join(dpath, self.__class__._index_fname)
        index_dtype = np.dtype([
            (self.__class__._post_no_srt_name,'i4'),('N','i4'),
            ('datetime_srt','U20'),('datetime_end','U20')
        ])
        if isfile(index_fpath):
            with open(index_fpath, 'rb') as f:
                index_arr_loaded = np.load(f, allow_pickle=True)
        else: index_arr_loaded = np.empty((0,), dtype=index_dtype)
            
        index_list = []
        for fpath, post_no_srt, N in data_file_info_arr:
            if post_no_srt not in index_arr_loaded[self.__class__._post_no_srt_name]:
                with open(fpath, 'rb') as f:
                    post_arr = np.load(f, allow_pickle=True)
                datetime_srt, datetime_end = post_arr[[0,-1]]['gall_date']
                index_list.append((post_no_srt,N,str(datetime_srt),str(datetime_end)))
                
        index_arr_add = np.array(index_list, dtype=index_dtype)
        index_arr_updated = np.concatenate((index_arr_loaded, index_arr_add))
        index_arr_updated.sort(order=self.__class__._post_no_srt_name)
        
        with open(index_fpath, 'wb') as f:
            np.save(f, index_arr_updated)

        # Check sync
        assert np.all(data_file_info_arr[self.__class__._post_no_srt_name] \
                      == index_arr_updated[self.__class__._post_no_srt_name])
        
        self.index = index_arr_updated
        
        
    def load_by_datetime(self, datetime_range_min, datetime_range_max):
        
        assert datetime_range_min < datetime_range_max
        
        #### Get indices where given datetime limits are located
        j_min, j_max = -1, -1

        for j_index, (_, _, dt_srt_str, dt_end_str) in enumerate(self.index):

            dt_srt, dt_end = (datetime.fromisoformat(s) 
                              for s in (dt_srt_str, dt_end_str))

            contains_min, contains_max = (
                not ((dt_srt > dt) or (dt > dt_end)) 
                for dt in (datetime_range_min, datetime_range_max)
            )
            if contains_min: j_min = j_index
            if contains_max: j_max = j_index

        assert (j_min >= 0) and (j_max >= 0)
        
        N_chunck = j_max - j_min + 1
        index_seg = self.index[j_min:j_min+N_chunck]
        
        # Check continuity of post numbers
        assert np.all((index_seg['post_no_srt'][:-1] + index_seg['N'][:-1]) \
                      == index_seg['post_no_srt'][1:])
        
        post_arr_list = []
        for path, _, _ in self.data[j_min:j_min+N_chunck]:
            with open(path, 'rb') as f:
                post_arr = np.load(f, allow_pickle=True)
            post_arr_list.append(post_arr)
        post_arr_tot = np.concatenate(post_arr_list)
        
        post_in_range_mask = (datetime_range_min <= post_arr_tot['gall_date']) \
            & (post_arr_tot['gall_date'] < datetime_range_max)
        post_arr_in_range = post_arr_tot[post_in_range_mask]
        
        return post_arr_in_range








def parse_gall_writer(tag_div_gall_writer):
    
    class_value = tag_div_gall_writer.get('class')
    assert class_value is not None
    assert 'gall_writer' in class_value
    
    data_uid, data_ip, data_nick = (tag_div_gall_writer.get(key) 
        for key in ('data-uid','data-ip','data-nick'))
    
    has_uid = data_uid != ''
    has_ip = data_ip != ''
    assert xor(has_uid, has_ip)
    
    img_fname = None
    if has_uid:
        tag_img_src = tag_div_gall_writer.find('img').get('src')
        assert tag_img_src is not None
        img_fname = tag_img_src.split('/')[-1].split('.')[0]
        
    return data_uid, data_ip, data_nick, img_fname

