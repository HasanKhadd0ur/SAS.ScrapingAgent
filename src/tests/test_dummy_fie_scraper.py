import pytest
import uuid
from app.agent import Agent
from app.core.configs.env_config import EnvConfig
from app.core.models.scraper_task import DataSource, ScrapingApproach, ScrapingTask
from app.core.configs.scrapers_config import DUMMY_SCRAPER_CONFIG
from app.scrapers.factory.scrapers_factory import ScraperFactory
from app.scrapers.sources.dummy.dummy_file_scrarper import DummyFileScraper
from app.pipeline.factory.default_pipelines import preprocessing_pipeline, publishing_pipeline

@pytest.mark.asyncio
async def test_dummy_file_scraper_loads_data():
    scraper = DummyFileScraper(EnvConfig())
    
    task = ScrapingTask(
                    id=str(uuid.uuid4()), 
                    platform='Telegram',
                    domain="politics",
                    sources=[DataSource(target="freesyria102", limit=30)],
                    limit=100,
                    scraping_approach=ScrapingApproach(name="DummyFileScraper",platform="File",mode="Dummy")
                )

    # Simulate task assignment
    agent = Agent(
        scraper=DummyFileScraper(EnvConfig()),
        preprocessing_pipeline=preprocessing_pipeline,
        publishing_pipeline=publishing_pipeline
    )
    factory = ScraperFactory()

    scraper = factory.create_scraper(task.scraping_approach)


    agent.set_scraper(scraper)
    agent.assign_task(task)
    
    await agent.run()
    
    assert isinstance("", str)
