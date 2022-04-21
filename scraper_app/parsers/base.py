from abc import ABC
from hashlib import sha1
from typing import Set

from bs4 import BeautifulSoup

from posting_app.database import Posting


class BaseParser(ABC):

    def __init__(self, base_url: str):
        self._base_url = base_url

    def get_soup_object(self, html: str):
        '''
        Taking HTML code as an entry, returns
        a BeautifulSoup object of the HTML code
        '''
        self.soup = BeautifulSoup(html, 'html.parser')
    
    def get_id(self, text: str) -> str:
        '''Get a SHA1 hash to identify each object.'''
        _id = sha1(text.lower().encode('utf-8')).hexdigest()
        return _id

    def extract_data(self) -> Set[Posting]:
        pass