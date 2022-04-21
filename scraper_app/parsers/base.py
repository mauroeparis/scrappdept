from abc import ABC
from hashlib import sha1

from bs4 import BeautifulSoup


class BaseParser(ABC):

    def __init__(self, base_url: str):
        self._base_url = base_url

    def get_soup_object(self, html):
        """
        Taking HTML code as an entry, returns
        a BeautifulSoup object of the HTML code
        """
        self.soup = BeautifulSoup(html, "html.parser")
    
    def get_id(self, text):
        """
        Get a SHA1 hash to identify each object.
        """
        _id = sha1(text.encode("utf-8")).hexdigest()
        return _id