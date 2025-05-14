from app.scrapers.base import BaseScraper
from app.core.models.scraper_task import ScrapingTask
from app.core.models.message import Message
from typing import AsyncGenerator, List
import json
import asyncio
import os

class DummyFileScraper(BaseScraper):
    def __init__(self, config: dict):
        self.config = config
        self.file_path = config.get("file_path", "../assets/sample_tweets.jsonl")
        self.delay = config.get("delay", 0.1)
        self.batch_size = config.get("batch_size", 1)

    async def run_task(self, task: ScrapingTask) -> AsyncGenerator[List[Message], None]:
        batch = []

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                for line in f:
                    await asyncio.sleep(self.delay)  # simulate delay
                    data = json.loads(line)

                    msg = Message(
                        id=data["tweet_id"],
                        source="dummy_file",
                        domain=task.domain,
                        platform="dummy_file",
                        raw_content=data["text"],
                        content=data["text"],
                        timestamp=data["created_at"]
                    )
                    batch.append(msg)

                    if len(batch) >= self.batch_size:
                        yield batch
                        batch = []

                if batch:
                    yield batch

        except Exception as e:
            print(f"Error reading dummy file: {e}")
