import asyncio
import uuid
from typing import AsyncGenerator
from app.core.models.scraper_task import ScraperTask, ScraperSource


class TasksService:
    def __init__(self, *args, **kwargs):
        pass  # No Kafka dependency for the dummy version

    async def stream_tasks(self) -> AsyncGenerator[ScraperTask, None]:
        # Simulate streaming 3 fake tasks with small delays
        for i in range(3):
            await asyncio.sleep(1)  # Simulate delay between tasks
            yield ScraperTask(
                    id=str(uuid.uuid4()), 
                    domain="politics",
                    sources=[ScraperSource(target="freesyria102", limit=10)],
                    limit=30
                )

