import asyncio
import uuid
from typing import AsyncGenerator
from app.core.models.scraper_task import DataSource, ScrapingApproach, ScrapingTask

class TasksService:
    def __init__(self, *args, **kwargs):
        pass  # No Kafka dependency for the dummy version

    async def stream_tasks(self) -> AsyncGenerator[ScrapingTask, None]:
        # Simulate streaming 3 fake tasks with small delays
        for i in range(300):
            # await asyncio.sleep(1)  # Simulate delay between tasks
            # yield ScrapingTask(
            #         id=str(uuid.uuid4()), 
            #         platform="telegram",
            #         domain="Politics",
            #         sources=[DataSource(target="freesyria102", limit=30)],
            #         limit=100,
            #         scraping_approach=ScrapingApproach(name="DummyFileScraper",platform="File",mode="Dummy")
            #     )
            # yield ScrapingTask(
            #         id=str(uuid.uuid4()), 
            #         platform="telegram",
            #         domain="Politics",
            #         sources=[
            #             # DataSource(target="freesyria102", limit=160),
            #             # DataSource(target="Almohrar", limit=1060),
            #             DataSource(target="MQ_QU", limit=160)
            #                  ],
            #         limit=100,
            #         scraping_approach=ScrapingApproach(name="TelegramWebScraper",platform="telegram",mode="Web")
            #     )
             yield ScrapingTask(
                    id=str(uuid.uuid4()), 
                    platform="telegram",
                    domain="Politics",
                    sources=[
                        # DataSource(target="freesyria102", limit=160),
                        # DataSource(target="Almohrar", limit=1060),
                        DataSource(target="MQ_QU", limit=160)
                             ],
                    limit=100,
                    scraping_approach=ScrapingApproach(name="TelegramTelethonScraper",platform="telegram",mode="bot")
                )
# Almohrar
# freesyria102
# MQ_QU