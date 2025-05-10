import asyncio
from app.agent import Agent
from app.scrapers.dummy.dummy_file_scrarper import DummyFileScraper
from app.pipeline.registry import preprocessing_pipeline, publishing_pipeline
from app.core.services.tasks_service import TasksService
from app.core.configs.scrapers_config import DUMMY_SCRAPER_CONFIG, TELEGRAM_WEB_SCRAPER_CONFIG
from app.scrapers.telegram.telegram_web_scraper import TelegramWebScraper

async def main():
    tasks_service = TasksService()

    agent = Agent(
        scraper=TelegramWebScraper(config=TELEGRAM_WEB_SCRAPER_CONFIG),
        preprocessing_pipeline=preprocessing_pipeline,
        publishing_pipeline=publishing_pipeline
    )

    async for task in tasks_service.stream_tasks():

        agent.assign_task(task)
        await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
