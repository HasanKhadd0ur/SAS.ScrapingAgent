from app.core.configs.env_config import EnvConfig
from app.core.models.scraper_task import ScrapingApproach
from app.scrapers.registry.scrapers_registry import ScraperRegistry
from app.scrapers.sources.dummy.dummy_file_scrarper import DummyFileScraper
from app.scrapers.sources.telegram.telegram_telethon_scraper import TelegramTelethonScraper
from app.scrapers.sources.telegram.telegram_web_scraper import TelegramWebScraper

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

        self.registry.register(
            ScrapingApproach(name="TelegramTelethonScraper", platform="telegram", mode="bot"),
            TelegramTelethonScraper,
            EnvConfig()
        )
    def create_scraper(self, approach: ScrapingApproach):
        return self.registry.get_scraper(approach)
