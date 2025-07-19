from typing import Dict, Type, Tuple
from app.core.configs.base_config import BaseConfig
from app.core.configs.env_config import EnvConfig
from app.core.models.scraper_task import ScrapingApproach
from app.scrapers.base.base_scraper import BaseScraper
from app.scrapers.sources.dummy.dummy_file_scrarper import DummyFileScraper

class ScraperRegistry:

    def __init__(self):
        self.registry: Dict[str, Tuple[Type[BaseScraper], dict]] = {}

    def register(self, approach: ScrapingApproach, scraper_class: Type[BaseScraper], config: BaseConfig= None):
        """
        Register a scraper along with its configuration.
        """
        key = self._make_key(approach)
        self.registry[key] = (scraper_class, config or EnvConfig())

    def get_scraper(self, approach: ScrapingApproach) -> BaseScraper:
        """
        Instantiate the scraper with its registered configuration.
        """
        key = self._make_key(approach)
        scraper_class, config = self.registry.get(key, (DummyFileScraper,EnvConfig()))
        return scraper_class(config_service=config)

    def _make_key(self, approach: ScrapingApproach) -> str:
        return f"{approach.platform.lower()}:{approach.mode.lower()}"
