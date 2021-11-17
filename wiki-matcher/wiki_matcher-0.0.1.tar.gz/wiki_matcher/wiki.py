import datetime
import typing
import requests
import re
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup as soup
from urllib3.exceptions import InsecureRequestWarning

class WikiItem(ABC):
    def __init__(self, name):
        self.name = name
    @abstractmethod
    def full_descr(self):
        pass
    def key_names(self):
        return [self.name]
    def __eq__(self, other):
        return self.name.lower() == other.name.lower()
    def __hash__(self):
        return hash(self.name.lower())

WikiItems = typing.List[WikiItem]

class WikiPage:
    def __init__(self, link, parser):
        self.items = {}
        self.max_word_cnt = 0
        self.link = link
        self.parser = parser
        self.ignorer = parser.ignorer
        
    def get_page_text(self):
        res = requests.get(self.link, verify=False)
        return soup(res.text, features="html.parser")
    
    def parse(self):
        self.items = {}
        items = self.parser.parse(self.get_page_text())
        for item in items:
            for name in item.key_names():
                name = re.sub('\s+', ' ', name.strip())
                word_len = name.count(' ') + 1
                self.max_word_cnt = max(self.max_word_cnt, word_len)
                self.items[name] = item

        self.max_word_cnt = max(self.max_word_cnt, self.ignorer.max_word_cnt())
           
        self.last_update = datetime.datetime.utcnow()
        return self.items

class Wiki:
    def __init__(self):
        self.force_update = False
        self._changed = False
        self.max_word_cnt = 0
        self._items = {}
        self.clear_items()
        self._pages = []

    def clear_items(self):
        self._items = {}
        self.max_word_cnt = 0

    def add_page(self, page):
        self._pages.append(page)
        self._changed = True

    def add_pages(self, pages):
        for page in pages:
            self.add_page(page)

    def update(self):
        self.clear_items()
        if self.want_update():
            for page in self._pages:
                page.parse()
                self._map_page(page)
        self.force_update = False
        self._changed = False

    def _map_page(self, page):
        for name in page.items:
            if name.lower() not in self._items:
                item = page.items[name]
                item.ignorer = page.ignorer
                self._items[name.lower()] = item
        self.max_word_cnt = max(self.max_word_cnt, page.max_word_cnt)

    def want_update(self):
        return self.force_update or self._changed

    def get_items(self):
        return self._items

    def start_force_update(self):
        self.force_update = True
        self.update()


def create_pages(links, parser):
    return [WikiPage(link, parser) for link in links]

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
