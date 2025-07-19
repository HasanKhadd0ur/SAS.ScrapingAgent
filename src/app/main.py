import asyncio
from app.agent import Agent
from app.core.configs.env_config import EnvConfig
from app.core.services.master_connection_service import MasterConnectionService
from app.core.services.tasks_service import TasksService
from app.scrapers.factory.scrapers_factory import ScraperFactory
from app.scrapers.sources.dummy.dummy_file_scrarper import DummyFileScraper
from app.pipeline.factory.default_pipelines import preprocessing_pipeline, publishing_pipeline

config = EnvConfig()

master_url = config.get_master_url()
scraper_name = config.get_scraper_name()
scraper_id=''

async def main():
    
    # connect to the master 
    master_service = MasterConnectionService(master_url, scraper_name)
    scraper_id = await master_service.connect()

    tasks_service = TasksService(master_api_url=config.get_master_url())
    factory = ScraperFactory()

    agent = Agent(
        scraper=DummyFileScraper(config_service=EnvConfig()),
        preprocessing_pipeline=preprocessing_pipeline,
        publishing_pipeline=publishing_pipeline
    )

    async for task in tasks_service.stream_tasks():
        await tasks_service.assign_executor(scraper_id=scraper_id,scraping_task_id=task.id)
        scraper = factory.create_scraper(task.scraping_approach)

        agent.set_scraper(scraper)
        agent.assign_task(task)
        await agent.run()
        await tasks_service.complete_task(task.id)

if __name__ == "__main__":
    
    asyncio.run(main())
