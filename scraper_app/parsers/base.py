from abc import ABC
from hashlib import sha1
from typing import Set

from bs4 import BeautifulSoup

from posting_app.database import Posting


class BaseParser(ABC):

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
    
    def sanitize_text(self, text):
        '''
        Sometimes the message comes out weirdly from the html
        this fixes it for you.
        '''
        return ' '.join(text.split())

    def extract_data(self) -> Set[Posting]:
        pass