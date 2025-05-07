# app/main.py
import asyncio
from app.core.models.scraper_task import ScraperSource, ScraperTask
from app.scrapers.nitter.nitter_web_scraper import NitterWebScraper
from app.scrapers.telegram.telegram_web_scraper import TelegramWebScraper

from app.pipeline.registry import default_pipeline  # Your pipeline

async def main():
    task = ScraperTask(
        domain="politics",
        sources=[ScraperSource(target="elonmusk")],
        limit=3
    )

    scraper = NitterWebScraper(credentials={})
    messages = await scraper.run_task(task)
    print(messages)
    for msg in messages:
        print(msg.content)
    
        processed = default_pipeline.process(msg)
        print("\nProcessed Message:\n", processed)

if __name__ == "__main__":
    asyncio.run(main())
