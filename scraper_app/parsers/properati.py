from typing import Set

from bs4 import BeautifulSoup

from .base import BaseParser
from posting_app.database import Posting, PostingRepository


class ProperatiParser(BaseParser):
    base_info_class = 'StyledCardInfo-sc-6ce7as-2'
    base_info_tag = 'div'
    link_regex = 'a'
    price_regex = 'div.StyledPrice-sc-6ce7as-5'
    location_regex = 'span.StyledLocation-sc-6ce7as-7'
    _base_url = 'https://www.properati.com.ar'

    def extract_data(self) -> Set[Posting]:
        '''Extracting data and returning list of postings'''
        postings = set()
        base_info_soaps = self.soup.find_all(
            self.base_info_tag, class_=self.base_info_class)

        for base_info_soap in base_info_soaps:
            try:
                link_container = base_info_soap.select(self.link_regex)[0]
                price_container = base_info_soap.select(self.price_regex)[0]
                location_container = base_info_soap.select(
                    self.location_regex)[0]
            except Exception as e:
                import ipdb;ipdb.set_trace()
                continue

            href = '{}{}'.format(
                self._base_url,
                link_container['href'],
            )
            title = self.sanitize_text(link_container.text)
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
