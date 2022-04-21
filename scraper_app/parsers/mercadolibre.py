from typing import Set

from bs4 import BeautifulSoup

from .base import BaseParser
from posting_app.database import Posting, PostingRepository


class MercadolibreParser(BaseParser):
    name = "Mercado Libre"
    url_base = "https://inmuebles.mercadolibre.com.ar"

    base_info_class = "ui-search-layout__item"
    base_info_tag = "li"
    link_regex = "a.ui-search-item__group__element"
    price_regex = "span.price-tag-fraction"
    description_regex = "ul.ui-search-card-attributes"
    location_regex = "span.ui-search-item__location"

    def extract_data(self) -> Set[Posting]:
        """Extracting data and returning list of objects"""
        postings = set()
        base_info_soaps = self.soup.find_all(
            self.base_info_tag, class_=self.base_info_class
        )

        for base_info_soap in base_info_soaps:
            try:
                link_container = base_info_soap.select(self.link_regex)[0]
                price_container = base_info_soap.select(self.price_regex)[0]
                description_container = base_info_soap.select(
                    self.description_regex)[0]
                location_container = base_info_soap.select(
                    self.location_regex)[0]
            except Exception as e:
                continue
            else:
                href = link_container["href"]
                sha = self.get_id(href.split("#")[0])
                price = self.sanitize_text(price_container.text)
                description = self.sanitize_text(description_container.text)
                location = self.sanitize_text(location_container.text)

                posting_repository = PostingRepository()
                if posting_repository.get_posting_by_sha(sha):
                    continue

                new_posting = Posting(
                    sha=sha,
                    url=href,
                    title=location,
                    price="$ %s" % price,
                    description=description,
                    location=location,
                )
                postings.add(new_posting)

        return postings