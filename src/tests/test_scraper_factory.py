from app.scrapers.factory import ScraperFactory
from app.core.models.scraper_task import ScrapingApproach
from app.scrapers.dummy.dummy_file_scrarper import DummyFileScraper

def test_factory_returns_dummy_scraper():
    approach = ScrapingApproach(name="DummyFileScraper", platform="File", mode="Dummy")
    factory = ScraperFactory()
    scraper = factory.create_scraper(approach)

    assert isinstance(scraper, DummyFileScraper)
    assert scraper.config["file_path"] == "../assets/mini-sample.jsonl"
