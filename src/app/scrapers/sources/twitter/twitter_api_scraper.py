import asyncio
import logging
from typing import AsyncGenerator, List
import tweepy.asynchronous
from app.core.configs.base_config import BaseConfig
from app.scrapers.base.base_scraper import BaseScraper
from app.core.models.scraper_task import ScrapingTask
from app.core.models.message import Message


class TwitterApiScraper(BaseScraper):
    def __init__(self, config_service: BaseConfig):
        self.config_service = config_service
        config = config_service.get_config("TWITTER_WEB_SCRAPER_CONFIG")

        self.batch_size = config.get("batch_size", 5)
        self.delay = config.get("delay", 0.1)
        self.logger = logging.getLogger(__name__)

        self.bearer_token = config.get("bearer_token")
        if not self.bearer_token:
            raise ValueError("Missing Twitter API Bearer Token.")

        self.client = tweepy.asynchronous.AsyncClient(bearer_token=self.bearer_token)

    async def run_task(self, task: ScrapingTask) -> AsyncGenerator[List[Message], None]:
        batch = []

        try:
            for source in task.sources:
                try:
                    self.logger.info(f"Scraping tweets from: {source.target}")
                    # Perform search (source.target is assumed to be a keyword or hashtag)
                    query = source.target
                    limit = source.limit or 10

                    response = await self.client.search_recent_tweets(
                        query=query,
                        max_results=min(limit, 100),
                        tweet_fields=["created_at", "text", "id"],
                    )

                    tweets = response.data or []

                    for tweet in tweets:
                        msg = Message(
                            id=str(tweet.id),
                            source=source.target,
                            domain=task.domain,
                            platform="twitter",
                            raw_content=tweet.text,
                            created_at=tweet.created_at.isoformat() if tweet.created_at else None,
                            content=tweet.text,
                        )
                        batch.append(msg)

                        if len(batch) >= self.batch_size:
                            yield batch
                            batch = []
                            await asyncio.sleep(self.delay)

                except Exception as e:
                    self.logger.error(f"Error while scraping from source {source.target}: {e}")

            if batch:
                yield batch

        except Exception as e:
            self.logger.exception("Failed to run Twitter scraper.")
