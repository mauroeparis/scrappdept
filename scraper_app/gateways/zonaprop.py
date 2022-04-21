from .base import BaseGateway


class ZonapropGateway(BaseGateway):
    def __init__(self, url: str):
        self._name = 'Zonaprop'
        self._base_url = 'https://www.zonaprop.com.ar'
        self._full_url = url
