import time

from connectors.argenprop import ArgenpropCrawler
from connectors.zonaprop import ZonapropCrawler
from connectors.mercadolibre import MercadolibreCrawler
#from connectors.olx import OlxCrawler

crawlers = [
    #OlxCrawler,
    ArgenpropCrawler,
    ZonapropCrawler,
    MercadolibreCrawler,
]

while True:
    for Crawler in crawlers:
        crawler_obj = Crawler()
        crawler_obj.do_ya_thing()

    time.sleep(60*10)



