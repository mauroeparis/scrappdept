import time

from hashlib import sha1
from urllib.parse import urlparse

import cloudscraper
import requests
from bs4 import BeautifulSoup
from requests.exceptions import InvalidSchema


class BaseCrawler:

    name = None
    url_base = None
    full_url = None

    base_info_class = None
    base_info_tag = None
    link_regex = None
    price_regex = None

    # Telegram bot token here
    bot_token = "1346325228:AAER2AItAePnwDod8E4wWgZ5RAguDlq67dA"
    # Chat roop ID goes here
    chat_room = "-1001351937287"

    soup = None

    def do_ya_thing(self):
        """
        Set of steps that the crawler needs to send the data.
        """
        print("Doing my thing now!")
        html = self.make_request()
        soup = self.get_soup_object(html)
        objects = self.extract_data(soup)
        seen, unseen = self.split_seen_and_unseen(objects)
        self.send_data(unseen)
        print("All done pal!")

    def make_request(self):
        """
        Makes the request to the full_url using cloudscraper
        and returns the html in it.
        """
        html = ""
        scraper = cloudscraper.create_scraper()
        print("Te traigo las cosas de: %s", self.full_url)

        try:
            res = scraper.get(self.full_url)
        except InvalidSchema as e:
            print("ERROR: No se pudo man. Aca te va: %s", e)
        else:
            if res.ok:
                html = res.text
                print("%s responded OK!", self.name)
            else:
                print(
                    "ERROR: %s responded with error %s!"
                    % self.name, res.status_code
                )

        return html

    def get_soup_object(self, html):
        """
        Taking HTML code as an entry, returns
        a BeautifulSoup object of the HTML code
        """
        self.soup = BeautifulSoup(html, "lxml")
        return self.soup

    def get_id(self, text):
        """
        Get a SHA1 hash to identify each object.
        """
        _id = sha1(text.encode("utf-8")).hexdigest()
        return _id

    def sanitize_text(self, text):
        """
        Sometimes the message comes out weirdly from the html
        this fixes it for you.
        """
        return ' '.join(text.split())

    def extract_data(self, soup):
        """
        Must be implemented in each child
        """
        raise NotImplementedError(
            "You must define the 'extract_data' function")

    def object_to_message(self, obj):
        """
        Formats the object into a Telegram message.
        """
        msg = ('<b>{}</b>\n<i>{}</i> - <i>{}</i>\n\n{}\n\n{}'.format(
            obj['title'],
            obj['price'],
            obj['location'],
            obj['description'],
            obj['url'],
        ))
        return msg

    def send_data(self, objects):
        """
        Transforms each object to a formatted Telegram message
        and if the bot is able to send the message, it marks the
        object as seen.
        """
        for obj in objects:
            msg = self.object_to_message(obj)
            res_ok = self.send_telegram_message(msg)
            if res_ok:
                self.mark_as_seen(obj)
            time.sleep(3.5)

    def send_telegram_message(self, text):
        """Sends text to Telegram group"""
        url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=html".format(
            self.bot_token, self.chat_room, text)
        res = requests.get(url)
        return res.ok

    def split_seen_and_unseen(self, objects):
        history = self.get_history()
        seen = [obj for obj in objects if obj["id"] in history]
        unseen = [obj for obj in objects if obj["id"] not in history]
        return seen, unseen

    def get_history(self):
        with open("seen.txt", "r") as f:
            return {l.rstrip() for l in f.readlines()}

    def mark_as_seen(self, obj):
        with open("seen.txt", "a+") as f:
            f.write("%s\n" % obj["id"])
        with open("seen_data.txt", "a+") as f:
            f.write("%s -> %s\n" % (obj["id"], obj["url"]))


