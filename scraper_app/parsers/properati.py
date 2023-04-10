from typing import Set

from bs4 import BeautifulSoup

from .base import BaseParser
from posting_app.database import Posting, PostingRepository


class ProperatiParser(BaseParser):
    #base_info_class = '' 
    base_info_tag = 'a'
    title_regex = 'div.listing-card__title'
    link_regex = 'a'
    price_regex = 'div.price'

    '''Description regexs'''
    description_regex = 'div.listing-card__information-bottom'
    properties_regex = 'div.properties'

    '''Location regexs'''
    location_regex = 'div.listing-card__location'
    location_regex_option2 = 'div.location'


    _base_url = 'https://www.properati.com.ar'

    def extract_data(self) -> Set[Posting]:
        '''Extracting data and returning list of postings'''
        postings = set()
        
        # Using onclick attribute instead of class
        base_info_soaps = self.soup.find_all(
            self.base_info_tag, {"onclick": True})

        for base_info_soap in base_info_soaps:
            try:
                title_container = base_info_soap.select(self.title_regex)[0]
                link_container = base_info_soap
                price_container = base_info_soap.select(self.price_regex)[0]

                # Location can be found either in location_regex or location_regex_option2
                if len(base_info_soap.select(self.location_regex))>0:
                    location_container =base_info_soap.select(self.location_regex)[0]
                elif base_info_soap.select(self.location_regex_option2) is not None:
                    location_container =base_info_soap.select(self.location_regex_option2)[0]

                '''Description can be found either in description_regex or properties_regex'''    
                if len(base_info_soap.select(self.description_regex))>0:
                    description_container = base_info_soap.select(self.description_regex)[0]    
                elif base_info_soap.select(self.properties_regex) is not None:
                    description_container = base_info_soap.select(self.properties_regex)[0]    
               

            except Exception as e:
                
                continue

            href = '{}{}'.format(
                self._base_url,
                link_container['href'],
            )
            title = self.sanitize_text(title_container.text)
            sha = self.get_id(href)
            price = self.sanitize_text(price_container.text)
            location = self.sanitize_text(location_container.text)
            description = self.sanitize_text(description_container.text)

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
