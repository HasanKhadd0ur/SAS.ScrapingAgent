import asyncio
import logging
from typing import AsyncGenerator, List
from telethon import TelegramClient
from app.core.configs.base_config import BaseConfig
from app.scrapers.base.base_scraper import BaseScraper
from app.core.models.scraper_task import ScrapingTask
from app.core.models.message import Message


class TelegramTelethonScraper(BaseScraper):
    def __init__(self, config_service: BaseConfig):
        self.config_service = config_service
        config = config_service.get_config("TELEGRAM_WEB_SCRAPER_CONFIG")

        self.batch_size = config.get("batch_size", 5)
        self.delay = config.get("delay", 0.1)
        self.logger = logging.getLogger(__name__)
        self.credential = config_service.get_random_telegram_credential()

        if not self.credential:
            raise ValueError("No Telegram credentials available in config.")

        self.client = TelegramClient(
            self.credential.session_name,
            self.credential.api_id,
            self.credential.api_hash
        )

    async def run_task(self, task: ScrapingTask) -> AsyncGenerator[List[Message], None]:
        try:
            # Connect with appropriate auth
            if self.credential.auth_type == "bot":
                if not self.credential.bot_token:
                    raise ValueError("Bot token is required for bot auth.")
                await self.client.start(bot_token=self.credential.bot_token)
            else:
                await self.client.start()

            batch = []

            for source in task.sources:
                try:
                    self.logger.info(f"Scraping from source: {source.target}")
                    channel = await self.client.get_entity(source.target)
                    await asyncio.sleep(2)  # Cooldown between entity fetches

                    async for message in self.client.iter_messages(channel, limit=source.limit):
                        await asyncio.sleep(0.5)  # Delay between messages

                        if not message or not message.text:
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
                    self.logger.error(f"Error while scraping source {source.target}: {e}")

            if batch:
                yield batch

        except Exception as e:
            self.logger.exception("Failed to initialize or run Telegram scraper.")
        finally:
            await self.client.disconnect()
