"""Parsing routines"""

import re
from itertools import chain


class VID_Parser(object):
    
    patterns_str = (
        r'^https://youtu.be/(.*)',
        r'^https://www.youtube.com/watch\?v=(.*)'
    )
    vidlen = 11
    
    def __init__(self):
        self.patterns = tuple(
            (re.compile(s) for s in self.__class__.patterns_str)
        )
        
    def parse(self, url):
        vid = None
        for patt in self.patterns:
            sres = re.search(patt, url)
            if sres:
                vid = sres.group(1)[:self.__class__.vidlen]
                if len(vid) != self.__class__.vidlen: vid = None
                break
        return vid




class YT_VID_Parser(object):
    
    netloc_yt_tup = ('youtu.be','www.youtube.com')
    url_form1 = r"https://www.youtube.com/watch\?v=([a-zA-Z0-9_\-]{{{}}})"
    url_form2 = r"https://youtu.be/([a-zA-Z0-9_\-]{{{}}})"
    url_forms = (url_form1, url_form2)
    YT_VID_LEN = 11
    
    def __init__(self):
        patt_strs = tuple(
            (url_form.format(self.__class__.YT_VID_LEN) 
             for url_form in self.__class__.url_forms)
        )
        self.patts = tuple((re.compile(s) for s in patt_strs))
    
    def parse(self, s):
        vids = set(
            chain.from_iterable((re.findall(patt, s) 
                                 for patt in self.patts))
        )
        return vids





def str_to_duration_seconds(duration_str):
    HMS = ['H','M','S']
    patt_str = 'PT' + ''.join(['([0-9]+)'+ss for ss in HMS if ss in duration_str])
    HMS_num = [3600, 60, 1]

    extracted = re.search(patt_str, duration_str).groups()

    duration_tot_seconds = 0
    j_d = 0
    for j, ss in enumerate(HMS):
        if ss in duration_str:
            duration_tot_seconds += int(extracted[j_d]) * HMS_num[j]
            j_d += 1
    return duration_tot_seconds

