import asyncio
from app.agent import Agent
from app.core.configs.env_config import EnvConfig
from app.scrapers.dummy.dummy_file_scrarper import DummyFileScraper
from app.pipeline.registry import preprocessing_pipeline, publishing_pipeline
from app.core.services.tasks_service import TasksService
from app.core.configs.scrapers_config import DUMMY_SCRAPER_CONFIG
from app.scrapers.factory import ScraperFactory

async def main():
    tasks_service = TasksService()
    factory = ScraperFactory()

    agent = Agent(
        scraper=DummyFileScraper(config_service=EnvConfig()),
        preprocessing_pipeline=preprocessing_pipeline,
        publishing_pipeline=publishing_pipeline
    )

    async for task in tasks_service.stream_tasks():
        scraper = factory.create_scraper(task.scraping_approach)

        agent.set_scraper(scraper)
        agent.assign_task(task)
        await agent.run()

if __name__ == "__main__":
    
    asyncio.run(main())
