from typing import Optional, List

from rich.console import Console

from .gateways import (
    BaseGateway,
    ZonapropGateway,
    ArgenpropGateway,
    MercadolibreGateway,
)
from .parsers import (
    BaseParser,
    ZonapropParser,
    ArgenpropParser,
    MercadolibreParser,
)
from posting_app.database import Posting

console = Console()


class ScraperService:
    def __init__(
        self,
        pages: int,
        url: str,
        gateway: BaseGateway,
        parser: BaseParser,
    ):
        self._pages = pages
        self._url = url
        self._gateway = gateway
        self._parser = parser

    def get_postings_from_scraper(self) -> List[Posting]:
        postings = set()
        pages = self._pages if self._gateway.paginated else 1

        for page in range(1, pages + 1):
            console.log(f'Page {page} of {pages}')
            html = self._gateway.make_request(
                url=self._url.format(page)
            )

            self._parser.get_soup_object(html=html)
            new_postings = self._parser.extract_data()
            console.log(f'Got {len(new_postings)} new postings')

            postings = postings.union(new_postings)

        return postings


class ScraperServiceFactory:
    @classmethod
    def build_for_zonaprop(
        cls,
        pages: int,
        full_url: str
    ) -> ScraperService:
        return ScraperService(
            pages=pages,
            url=full_url,
            gateway=ZonapropGateway(),
            parser=ZonapropParser(),
        )

    @classmethod
    def build_for_argenprop(
        cls,
        pages: int,
        full_url: str
    ) -> ScraperService:
        return ScraperService(
            pages=pages,
            url=full_url,
            gateway=ArgenpropGateway(),
            parser=ArgenpropParser(),
        )

    @classmethod
    def build_for_mercadolibre(
        cls,
        pages: int,
        full_url: str
    ) -> ScraperService:
        return ScraperService(
            pages=pages,
            url=full_url,
            gateway=MercadolibreGateway(),
            parser=MercadolibreParser(),
        )