from typing import Optional, List

from .gateways import (
    BaseGateway,
    ZonapropGateway
)
from .parsers import (
    BaseParser,
    ZonapropParser,
)
from posting_app.database import Posting


class ScraperService:
    def __init__(
        self,
        url: str,
        gateway: BaseGateway,
        parser: BaseParser,
    ):
        self._url = url
        self._gateway = gateway
        self._parser = parser

    def get_postings_from_scraper(self) -> List[Posting]:
        html = self._gateway.make_request(url=self._url)

        self._parser.get_soup_object(html=html)
        postings = self._parser.extract_data()

        return postings


class ScraperServiceFactory:
    @classmethod
    def build_for_zonaprop(
        cls,
        base_url: str,
        full_url: str
    ) -> ScraperService:
        return ScraperService(
            url=full_url,
            gateway=ZonapropGateway(url=full_url),
            parser=ZonapropParser(base_url=base_url),
        )