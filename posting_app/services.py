from rich.console import Console

from .database import PostingRepository
from scraper_app.services import ScraperService

console = Console()


class PostingService:
    def __init__(self, scraper_service: ScraperService):
        self._scraper_service = scraper_service
    
    def scrap_and_create_postings(self):
        postings = self._scraper_service.get_postings_from_scraper()
        posting_repository = PostingRepository()

        console.log(f'About to save {len(postings)} postings')
        for posting in postings:
            posting_repository.create_posting(posting)
        console.log('Postings saved successfully!', style='green')


