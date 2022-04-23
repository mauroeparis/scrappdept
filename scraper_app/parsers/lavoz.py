from typing import Set

from bs4 import BeautifulSoup

from .base import BaseParser
from posting_app.database import Posting, PostingRepository


class LaVozParser(BaseParser):
    base_info_class = 'postingCardContent'
    url_base = "https://clasificados.lavoz.com.ar"

    base_info_class = "card-body"
    base_info_tag = "div"
    link_regex = "a"
    price_regex = "span.price"
    # description_regex = "p.card__info "
    location_regex = "div.h5"
    title_regex = "h2.h4"

    def extract_data(self) -> Set[Posting]:
        """Extracting data and returning list of objects"""
        postings = set()
        base_info_soaps = self.soup.find_all(
            self.base_info_tag, class_=self.base_info_class)

        for base_info_soap in base_info_soaps:
            try:
                link_container = base_info_soap.findParent(
                    'a'
                )
                price_container = base_info_soap.select(self.price_regex)[0]
                location_container = base_info_soap.select(
                    self.location_regex)[0]
                title_container = base_info_soap.select(
                    self.title_regex
                )[0]
            except Exception as e:
                continue
            else:
                href = "{}{}".format(
                    self.url_base, link_container.get("href"))
                title = self.sanitize_text(title_container.text)
                sha = self.get_id(href)
                price = self.sanitize_text(price_container.text)
                location = self.sanitize_text(location_container.text)

                posting_repository = PostingRepository()
                if posting_repository.get_posting_by_sha(sha):
                    continue

                new_posting = Posting(
                    sha=sha,
                    url=href,
                    title=title,
                    price=price,
                    location=location,
                )
                postings.add(new_posting)

        return postings
