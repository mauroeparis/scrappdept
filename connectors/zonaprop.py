from .base import BaseCrawler
import requests


class ZonapropCrawler(BaseCrawler):
    name = "Zonaprop"
    url_base = "https://www.zonaprop.com.ar"
    _full_url = (
        "https://www.zonaprop.com.ar/casas-"
        "departamentos-alquiler-cordoba-cb-desde"
        "-2-habitaciones-mas-de-2-ambientes-15000-25000-pesos"
        "-orden-publicado-descendent-pagina-{}.html"
    )
    number_of_pages = 0

    base_info_class = "postingCardContent"
    base_info_tag = "div"
    link_regex = "a.go-to-posting"
    price_regex = "span.firstPrice"
    description_regex = "div.postingCardDescription"
    location_regex = "span.postingCardLocation"

    def do_ya_thing(self):
        print("Doing my thing now!")
        for page in range(self.number_of_pages):
            self.full_url = self._full_url.format(page)
            print(self.full_url)
            html = self.make_request()
            soup = self.get_soup_object(html)
            objects = self.extract_data(soup)
            seen, unseen = self.split_seen_and_unseen(objects)
            self.send_data(unseen)
            print("All done pal!")
            print("=================================")

    def extract_data(self, soup):
        """Extracting data and returning list of objects"""
        objects = []
        base_info_soaps = soup.find_all(
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
                print("ERROR: the regex didnt work")
                continue
            else:
                href = "{}{}".format(
                    self.url_base, link_container["href"])
                title = self.sanitize_text(link_container.text)
                _id = self.get_id(href)
                price = price_container["data-price"]
                description = self.sanitize_text(description_container.text)
                location = self.sanitize_text(location_container.text)

                new_object = {
                    "id": _id,
                    "url": href,
                    "title": title,
                    "price": price,
                    "description": description,
                    "location": location,
                }

                if _id not in {obj["id"] for obj in objects}:
                    objects.append(new_object)

        return  objects


