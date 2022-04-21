from typing import Set

from bs4 import BeautifulSoup

from .base import BaseParser
from posting_app.database import Posting, PostingRepository


class ZonapropParser(BaseParser):
    base_info_class = 'postingCardContent'
    base_info_tag = 'div'
    link_regex = 'a.go-to-posting'
    price_regex = 'span.firstPrice'
    description_regex = 'div.postingCardDescription'
    location_regex = 'span.postingCardLocation'
    _base_url = 'https://www.zonaprop.com.ar/'

    def extract_data(self) -> Set[Posting]:
        '''Extracting data and returning list of postings'''
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
            except Exception as e:
                print('ERROR: the regex didnt work')
                continue

            href = '{}{}'.format(
                self._base_url,
                link_container['href'],
            )
            title = self.sanitize_text(link_container.text)
            sha = self.get_id(href)
            price = price_container['data-price']
            description = self.sanitize_text(description_container.text)
            location = self.sanitize_text(location_container.text)

            posting_repository = PostingRepository()
            if posting_repository.get_posting_by_sha(sha):
                continue

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
