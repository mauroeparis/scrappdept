from typing import Optional, List

from rich.console import Console

from .gateways import (
    BaseGateway,
    ZonapropGateway
)
from .parsers import (
    BaseParser,
    ZonapropParser,
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

        for page in range(1, self._pages + 1):
            console.log(f'Page {page} of {self._pages}')
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
        base_url: str,
        full_url: str
    ) -> ScraperService:
        return ScraperService(
            pages=pages,
            url=full_url,
            gateway=ZonapropGateway(),
            parser=ZonapropParser(base_url=base_url),
        )