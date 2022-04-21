from typing import Set

from bs4 import BeautifulSoup

from .base import BaseParser
from posting_app.database import Posting, PostingRepository


class ArgenpropParser(BaseParser):
    base_info_class = 'postingCardContent'
    url_base = "https://www.argenprop.com"

    base_info_class = "listing__item"
    base_info_tag = "div"
    link_regex = "a"
    price_regex = "p.card__price"
    description_regex = "p.card__info "
    location_regex = "h2.card__address"
    title_regex = "p.card__title"

    def extract_data(self) -> Set[Posting]:
        """Extracting data and returning list of objects"""
        postings = set()
        base_info_soaps = self.soup.find_all(
            self.base_info_tag, class_=self.base_info_class)

        for base_info_soap in base_info_soaps:
            try:
                link_container = base_info_soap.select(self.link_regex)[0]
                price_container = base_info_soap.select(self.price_regex)[0]
                description_container = base_info_soap.select(
                    self.description_regex)[0]
                location_container = base_info_soap.select(
                    self.location_regex)[0]
                title_container = base_info_soap.select(
                    self.title_regex
                )[0]
            except Exception as e:
                continue
            else:
                href = "{}{}".format(
                    self.url_base, link_container["href"])
                title = self.sanitize_text(title_container.text)
                sha = self.get_id(href)
                price = self.sanitize_text(price_container.text)
                description = self.sanitize_text(description_container.text)
                location = self.sanitize_text(location_container.text)

                new_posting = Posting(
                    sha=sha,
                    url=href,
                    title=title,
                    price=price,
                    description=description,
                    location=location,
                )
                postings.add(new_posting)

        return postings
