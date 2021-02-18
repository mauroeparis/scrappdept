import scrapy
import json
import urllib.parse
import requests

from scrapy.crawler import CrawlerProcess


class Olx(scrapy.Spider):
    name = 'olx'
    url = 'https://www.olx.com.ar/api/relevance/search?category=363&facet_limit=100&location=2006505&location_facet_limit=20&price_max=45000&sorting=desc-creation'

    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.87 Safari/537.36'
    }

    def start_requests(self):
        for page in range(5):
            yield scrapy.Request(self.url + '&page={}'.format(page), headers=self.headers, callback=self.parse)

    def parse(self, res):
        offers = []
        old_offers = []
        data = res.text
        data = json.loads(data)

        with open('offers.json', 'r') as offers_json:
            old_data = offers_json.read()
            if old_data:
                old_offers = json.loads(old_data)
            for offer in data['data']:
                to_add = True
                new_item = {
                    'title': offer['title'],
                    'date': offer['display_date'],
                    'description': offer['description'],
                    'id': offer['id'],
                    'location': offer['locations_resolved']['ADMIN_LEVEL_3_name'],
                    'price': offer['price']['value']['display'],
                    'url': 'https://www.olx.com.ar/item/' + offer['id'],
                    'send': False,
                }
                if old_offers:
                    for old_item in old_offers:
                        if old_item['id'] == new_item['id']:
                            to_add = False
                            break
                if to_add:
                    old_offers.append(new_item)
                    offers.append(new_item)

        with open('offers.json', 'w') as offers_json:
            offers = json.dumps(offers, indent=2)
            old_offers = json.dumps(old_offers, indent=2)
            offers_json.write(old_offers)
            formatter(offers)


def formatter(array_data):
    array_data = json.loads(array_data)
    for item in array_data:
        msg = ('<b>{}</b>\n<i>{}</i> - <i>{}</i>\n\n{}\n\n{}'.format(
            item['title'],
            item['price'],
            item['location'],
            item['description'],
            item['url'],
        ))
        parsed_data = urllib.parse.quote(msg)
        notify(parsed_data, item['id'])

def set_as_send(id):
    readed_json = {}
    with open('offers.json', 'w') as offers_json:
        readed_data = offers_json.reads()
        readed_json = json.loads(readed_data)


def notify(ad, id):
    bot = ""
    room = ""
    url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=html".format(bot, room, ad)
    r = requests.get(url)
    if r.ok:
        print("BARBARO MIREI TEAMO capo")

    else:
        print("Que mauro lechuza y boton, casi me salgo con la mia")
    time.sleep(3.5)

# run scraper
process = CrawlerProcess()
process.crawl(Olx)
process.start()

# debug
#Olx.parse(Olx, '')
