import json
from typing import Optional

import typer
from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError
from rich.console import Console
from rich.progress import track

from scraper_app.services import ScraperServiceFactory
from posting_app.database import create_db_and_tables, PostingRepository
from posting_app.services import PostingService
from telegram_app.services import TelegramService

console = Console()


class Config(BaseModel):
    pages: int
    bot_token: str
    chat_room: str
    zonaprop_base_url: Optional[str] = None
    zonaprop_full_url: Optional[str] = None


def main(config_path: str):
    # LOAD CONFIG
    with open(config_path) as config_json:
        config_dict = json.load(config_json)

    try:
        config = Config(**config_dict)
    except ValidationError as ex:
        console.log(
            '[bold u]ERROR[/bold u]: Config error.\n', ex, style='red'
        )
        return
    console.log('Configuration read correctly', style='italic bold green')
    
    # LOAD DATABASE
    create_db_and_tables()
    console.log('Database loaded', style='italic bold green')

    # SCRAP POSTINGS
    zonaprop_scraper_service = ScraperServiceFactory.build_for_zonaprop(
        pages=config.pages,
        base_url=config.zonaprop_base_url,
        full_url=config.zonaprop_full_url,
    )
    posting_service = PostingService(
        scraper_service=zonaprop_scraper_service
    )
    posting_service.scrap_and_create_postings()
    console.log('Postings scrapped', style='italic bold green')

    # SEND POSTINGS
    posting_repository = PostingRepository()
    unsent_postings = posting_repository.get_unsent_postings()

    # telegram_service = TelegramService(
    #     bot_token=config.bot_token,
    #     chat_room=config.chat_room,
    # )
    # console.log(f'About to send [u]{len(unsent_postings)}[/u] postings')
    # for posting in track(unsent_postings, description='Sending postings...'):
    #     msg_text = telegram_service.format_posting_to_message(posting)
    #     sent = telegram_service.send_telegram_message(msg_text)
    #     if sent:
    #         posting_repository.set_posting_as_sent(posting.sha)
    #         console.log(f'{posting.title} has been sent!', style='green')
    #     else:
    #         console.log(
    #             f'[bold u]ERROR[/bold u]: Unable to send {posting.title}',
    #             style='red'
    #         )
    console.log('Postings sent', style='italic bold green')


if __name__ == '__main__':
    typer.run(main)