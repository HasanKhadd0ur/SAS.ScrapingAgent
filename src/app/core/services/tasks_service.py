import asyncio
import uuid
from typing import AsyncGenerator
from app.core.models.scraper_task import DataSource, ScrapingApproach, ScrapingTask

class TasksService:
    def __init__(self, *args, **kwargs):
        pass  # No Kafka dependency for the dummy version

    async def stream_tasks(self) -> AsyncGenerator[ScrapingTask, None]:
        # Simulate streaming 3 fake tasks with small delays
        for i in range(3):
            await asyncio.sleep(1)  # Simulate delay between tasks
            yield ScrapingTask(
                    id=str(uuid.uuid4()), 
                    domain="telegram.Politics",
                    sources=[DataSource(target="freesyria102", limit=30)],
                    limit=100,
                    scraping_approach=ScrapingApproach(name="DummyFileScraper",platform="File",mode="Dummy")
                )
            # yield ScrapingTask(
            #         id=str(uuid.uuid4()), 
            #         domain="telegram.Politics",
            #         sources=[DataSource(target="freesyria102", limit=100)],
            #         limit=100,
            #         scraping_approach=ScrapingApproach(name="TelegramWebScraper",platform="Telegram",mode="Web")
            #     )

