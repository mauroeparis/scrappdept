from .database import PostingRepository
from scraper_app.services import ScraperService


class PostingService:
    def __init__(self, scraper_service: ScraperService):
        self._scraper_service = scraper_service
    
    def scrap_and_create_postings(self):
        postings = self._scraper_service.get_postings_from_scraper()
        posting_repository = PostingRepository()

        for posting in postings:
            posting_repository.create_posting(posting)


