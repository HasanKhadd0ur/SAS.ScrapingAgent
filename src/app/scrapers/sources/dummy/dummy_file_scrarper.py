from random import randint
from app.scrapers.base.base_scraper import BaseScraper
from app.core.models.scraper_task import ScrapingTask
from app.core.configs.base_config import BaseConfig
from app.core.models.message import Message
from typing import AsyncGenerator, List
import asyncio
import json


class DummyFileScraper(BaseScraper):
    def __init__(self, config_service: BaseConfig):
        config=config_service.get_config("DUMMY_SCRAPER_CONFIG")
        self.config = config
        self.file_path = config.get("file_path", "assets/sample_tweets.jsonl")
        self.delay = config.get("delay", 0.1)
        self.batch_size = config.get("batch_size", 1)

    async def run_task(self, task: ScrapingTask) -> AsyncGenerator[List[Message], None]:
        batch = []
        total_yielded = 0         
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if total_yielded >= task.limit:
                        break
                    await asyncio.sleep(self.delay+float(randint(1,40))/1000)  # simulate delay
                    data = json.loads(line)

                    msg = Message(
                        id=data["tweet_id"],
                        source="dummy_file",
                        domain=task.domain,
                        platform="dummy_file",
                        raw_content=data["text"],
                        content=data["text"],
                        created_at=data["created_at"]
                    )
                    
                    batch.append(msg)
                    total_yielded += 1
                    if len(batch) >= self.batch_size:
                        yield batch
                        batch = []

                if batch:
                    yield batch

        except Exception as e:
            print(f"Error reading dummy file: {e}")
