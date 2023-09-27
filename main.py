import yaml
from time import sleep
from typing import Optional

import typer
from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError
from rich.console import Console
from rich.progress import track

from posting_app.database import create_database, create_db_and_tables, PostingRepository
from posting_app.services import PostingServiceFactory
from telegram_app.services import TelegramService

console = Console()


class Config(BaseModel):
    pages: Optional[int] = 3
    sleep_time: Optional[int] = 5
    bot_token: str
    chat_room: str
    persist: Optional[bool] = False
    zonaprop_base_url: Optional[str] = None
    zonaprop_full_url: Optional[str] = None
    argenprop_full_url: Optional[str] = None
    mercadolibre_full_url: Optional[str] = None
    la_voz_full_url: Optional[str] = None
    properati_full_url: Optional[str] = None
    database_filename: Optional[str] = 'scrapdep'


def main(config_path: str):
    # LOAD CONFIG
    with open(config_path) as config_json:
        config_dict = yaml.safe_load(config_json)

    try:
        config = Config(**config_dict)
    except ValidationError as ex:
        console.log(
            '[bold u]ERROR[/bold u]: Config error.\n', ex, style='red'
        )
        return
    console.log('Configuration read correctly', style='italic bold green')
    
    # CREATE DATABASE
    create_database(config.database_filename)  

    # LOAD DATABASE
    create_db_and_tables()
    console.log('Database loaded', style='italic bold green')

    while(True):
        # SCRAP POSTINGS
        if config.zonaprop_full_url:
            zonaprop_posting_service = PostingServiceFactory.build_for_zonaprop(
                pages=config.pages,
                full_url=config.zonaprop_full_url,
            )
            zonaprop_posting_service.scrap_and_create_postings()

        if config.argenprop_full_url:
            argenprop_posting_service = PostingServiceFactory.build_for_argenprop(
                pages=config.pages,
                full_url=config.argenprop_full_url,
            )
            argenprop_posting_service.scrap_and_create_postings()

        if config.mercadolibre_full_url:
            mercadolibre_posting_service = PostingServiceFactory.build_for_mercadolibre(
                pages=config.pages,
                full_url=config.mercadolibre_full_url,
            )
            mercadolibre_posting_service.scrap_and_create_postings()

        if config.la_voz_full_url:
            la_voz_posting_service = PostingServiceFactory.build_for_la_voz(
                pages=config.pages,
                full_url=config.la_voz_full_url,
            )
            la_voz_posting_service.scrap_and_create_postings()

        if config.properati_full_url:
            properati_posting_service = PostingServiceFactory.build_for_properati(
                pages=config.pages,
                full_url=config.properati_full_url,
            )
            properati_posting_service.scrap_and_create_postings()

        console.log('Postings scrapped', style='italic bold green')

        # SEND POSTINGS
        posting_repository = PostingRepository()
        unsent_postings = posting_repository.get_unsent_postings()

        telegram_service = TelegramService(
            bot_token=config.bot_token,
            chat_room=config.chat_room,
        )
        console.log(f'About to send [u]{len(unsent_postings)}[/u] postings')
        for posting in track(unsent_postings, description='Sending postings...'):
            msg_text = telegram_service.format_posting_to_message(posting)
            sent = telegram_service.send_telegram_message(msg_text)
            if sent:
                posting_repository.set_posting_as_sent(posting.sha)
            else:
                console.log(
                    (
                        '[bold u]WARNING[/bold u]: '
                        f'Unable to send {posting.title}. '
                        'I\'m going to try later though, [u]don\'t panic[/u]'
                    ),
                    style='yellow'
                )
        console.log('Postings sent', style='italic bold green')

        if not config.persist:
            break
        
        sleep(config.sleep_time)


if __name__ == '__main__':
    typer.run(main)