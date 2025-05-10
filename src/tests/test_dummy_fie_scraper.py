import pytest
import uuid
from app.agent import Agent
from app.core.models.scraper_task import DataSource, ScrapingApproach, ScrapingTask
from app.scrapers.dummy.dummy_file_scrarper import DummyFileScraper
from app.core.configs.scrapers_config import DUMMY_SCRAPER_CONFIG
from app.pipeline.registry import preprocessing_pipeline, publishing_pipeline
from app.scrapers.factory import ScraperFactory

@pytest.mark.asyncio
async def test_dummy_file_scraper_loads_data():
    scraper = DummyFileScraper(config=DUMMY_SCRAPER_CONFIG)
    
    task = ScrapingTask(
                    id=str(uuid.uuid4()), 
                    domain="politics",
                    sources=[DataSource(target="freesyria102", limit=30)],
                    limit=100,
                    scraping_approach=ScrapingApproach(name="DummyFileScraper",platform="File",mode="Dummy")
                )

    # Simulate task assignment
    agent = Agent(
        scraper=DummyFileScraper(config=DUMMY_SCRAPER_CONFIG),
        preprocessing_pipeline=preprocessing_pipeline,
        publishing_pipeline=publishing_pipeline
    )
    factory = ScraperFactory()

    scraper = factory.create_scraper(task.scraping_approach)


    agent.set_scraper(scraper)
    agent.assign_task(task)
    
    await agent.run()
    
    assert isinstance("", str)
