from app.core.configs.env_config import EnvConfig
from app.core.models.scraper_task import ScrapingApproach
from app.scrapers.dummy.dummy_file_scrarper import DummyFileScraper
from app.scrapers.telegram.telegram_web_scraper import TelegramWebScraper
from app.scrapers.registry import ScraperRegistry
from app.core.configs.scrapers_config import DUMMY_SCRAPER_CONFIG, TELEGRAM_WEB_SCRAPER_CONFIG

class ScraperFactory:
    def __init__(self):
        self.registry = ScraperRegistry()
        self._register_defaults()

    def _register_defaults(self):
        self.registry.register(
            ScrapingApproach(name="DummyFileScraper", platform="File", mode="Dummy"),
            DummyFileScraper,
            EnvConfig()
        )

        self.registry.register(
            ScrapingApproach(name="TelegramWebScraper", platform="telegram", mode="web"),
            TelegramWebScraper,
            EnvConfig()
        )

    def create_scraper(self, approach: ScrapingApproach):
        return self.registry.get_scraper(approach)
