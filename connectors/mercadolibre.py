
from .base import BaseCrawler
import requests


class MercadolibreCrawler(BaseCrawler):
    name = "Mercado Libre"
    url_base = "https://inmuebles.mercadolibre.com.ar"
    full_url = (
        "https://inmuebles.mercadolibre.com.ar/casas/"
        "alquiler/cordoba/cordoba/nueva-cordoba-o-"
        "alta-cordoba-o-centro-o-general-paz-o-cofico"
        "/_DisplayType_LF_PriceRange_10000ARS-55000ARS"
    )

    base_info_class = "ui-search-layout__item"
    base_info_tag = "li"
    link_regex = "a.ui-search-item__group__element"
    price_regex = "span.price-tag-fraction"
    description_regex = "ul.ui-search-card-attributes"
    location_regex = "span.ui-search-item__location"

    def do_ya_thing(self):
        print("Doing my thing now!")
        html = self.make_request()
        soup = self.get_soup_object(html)
        objects = self.extract_data(soup)
        seen, unseen = self.split_seen_and_unseen(objects)
        self.send_data(unseen)
        print("All done pal!")

    def extract_data(self, soup):
        """Extracting data and returning list of objects"""
        objects = []
        base_info_soaps = soup.find_all(
            self.base_info_tag, class_=self.base_info_class)
        print("Lets get this MFO data!")

        for base_info_soap in base_info_soaps:
            try:
                link_container = base_info_soap.select(self.link_regex)[0]
                price_container = base_info_soap.select(self.price_regex)[0]
                description_container = base_info_soap.select(
                    self.description_regex)[0]
                location_container = base_info_soap.select(
                    self.location_regex)[0]
            except Exception as e:
                print("ERROR: the regex didnt work")
                continue
            else:
                href = link_container["href"]
                _id = self.get_id(href.split("#")[0])
                price = self.sanitize_text(price_container.text)
                description = self.sanitize_text(description_container.text)
                location = self.sanitize_text(location_container.text)

                new_object = {
                    "id": _id,
                    "title": location,
                    "url": href,
                    "price": "$ %s" % price,
                    "description": description,
                    "location": location,
                }

                if _id not in {obj["id"] for obj in objects}:
                    objects.append(new_object)

        return  objects

