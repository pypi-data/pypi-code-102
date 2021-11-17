from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from .ignore import Ignorer
from .wiki import WikiItems

default_ignorer = Ignorer()
class PageParser(ABC):
    def __init__(self, ignorer=default_ignorer):
        self.ignorer = ignorer
        
    @abstractmethod
    def find_items(self, soup: BeautifulSoup):
        pass
    @abstractmethod
    def create_item(self, data):
        pass
    
    def parse(self, soup: BeautifulSoup)->WikiItems:
        items = []
        for data in self.find_items(soup):
            item = self.create_item(data)
            if not self.ignorer.want_ignore(item.name):
                item.ignorer = self.ignorer
                items.append(item)
        return items
