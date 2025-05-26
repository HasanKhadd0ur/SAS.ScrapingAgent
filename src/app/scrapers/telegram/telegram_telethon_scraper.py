from time import sleep
from app.core.configs.base_config import BaseConfig
from app.scrapers.base import BaseScraper
from app.core.models.scraper_task import ScrapingTask
from app.core.models.message import Message
from typing import AsyncGenerator, List
import asyncio
from telethon import TelegramClient
import logging


class TelegramTelethonScraper(BaseScraper):
    def __init__(self, config_service: BaseConfig):
        config = config_service.get_config("TELEGRAM_WEB_SCRAPER_CONFIG")
        self.batch_size = config.get("batch_size", 5)
        self.api_id, self.api_hash = config_service.get_api_key()      
        self.delay = config.get("delay", 0.1)
        self.client = TelegramClient('anon_session', self.api_id, self.api_hash)
        self.logger = logging.getLogger(__name__)

    async def run_task(self, task: ScrapingTask) -> AsyncGenerator[List[Message], None]:
        await self.client.start()
        batch = []

        for source in task.sources:
            try:
                # Get entity for the channel username
                channel = await self.client.get_entity(source.target)
                sleep(50)
                # Iterate over messages, limit by source.limit
                async for message in self.client.iter_messages(channel, limit=source.limit):
                    sleep(3)
               
                    if message is None or message.text is None:
                        continue
                    
                    msg = Message(
                        id=str(message.id),
                        source=source.target,
                        domain=task.domain,
                        platform="telegram",
                        raw_content=message.text,
                        created_at=message.date.isoformat() if message.date else None,
                        content=message.text,
                    )
                    batch.append(msg)

                    if len(batch) >= self.batch_size:
                        yield batch
                        batch = []
                        await asyncio.sleep(self.delay)

            except Exception as e:
                self.logger.error(f"Failed to scrape channel {source.target}: {e}")

        if batch:
            yield batch

        await self.client.disconnect()
