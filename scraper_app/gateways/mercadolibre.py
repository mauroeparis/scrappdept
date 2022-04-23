from .base import BaseGateway


class MercadolibreGateway(BaseGateway):
    paginated = False

    def __init__(self):
        self._name = 'Mercadolibre'
