
from .base import BaseCrawler
import requests


class ArgenpropCrawler(BaseCrawler):
    name = "Argenprop"
    url_base = "https://www.argenprop.com"
    _full_url = (
        "https://www.argenprop.com/departamento-y-casa"
        "-alquiler-barrio-centro-cor-barrio-guemes-"
        "cor-barrio-jardin-barrio-nueva-cordoba-10000-55000-pesos"
        "-orden-masnuevos-pagina-{}"
    )
    number_of_pages = 5

    base_info_class = "listing__item"
    base_info_tag = "div"
    link_regex = "a"
    price_regex = "p.card__price"
    description_regex = "p.card__info "
    location_regex = "h2.card__address"
    title_regex = "h3.card__title"

    def do_ya_thing(self):
        print("Doing my thing now!")
        for page in range(1,self.number_of_pages,1):
            self.full_url = self._full_url.format(page)
            print(self.full_url)
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
                title_container = base_info_soap.select(
                    self.title_regex
                )[0]
            except Exception as e:
                continue
            else:
                href = "{}{}".format(
                    self.url_base, link_container["href"])
                title = self.sanitize_text(title_container.text)
                _id = self.get_id(href)
                price = self.sanitize_text(price_container.text)
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
