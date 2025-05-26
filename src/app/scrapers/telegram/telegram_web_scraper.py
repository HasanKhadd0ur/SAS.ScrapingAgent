from time import sleep
from app.core.configs.base_config import BaseConfig
from app.scrapers.base import BaseScraper
from app.core.models.scraper_task import ScrapingTask
from app.core.models.message import Message
from typing import AsyncGenerator, List
from playwright.async_api import async_playwright
import asyncio
from random import randint


class TelegramWebScraper(BaseScraper):
    def __init__(self, config_service: BaseConfig):
        config=config_service.get_config("TELEGRAM_WEB_SCRAPER_CONFIG")
        self.batch_size = config.get_config("batch_size", 5)
        self.delay = config.get("delay", 0.1)
        self.selector = config.get("selector", "div.tgme_widget_message_text")

    async def run_task(self, task: ScrapingTask) -> AsyncGenerator[List[Message], None]:
        batch = []

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            for source in task.sources:
                channel_url = f"https://t.me/s/{source.target}"

                await page.goto(channel_url)
                await page.wait_for_timeout(int(self.delay * 1000)+ randint(100,1000))  # convert to ms

                posts = await page.query_selector_all(self.selector)
                
                for post in posts[-source.limit:]:
                    # sleep(10)
                    # Extract message ID
                    data_post = await post.get_attribute("data-post")
                    message_id = data_post.split("/")[-1] if data_post else None

                    # Extract content text
                    content_element = await post.query_selector("div.tgme_widget_message_text")
                    content = await content_element.inner_text() if content_element else ""

                    # Extract author
                    author_element = await post.query_selector("div.tgme_widget_message_author span")
                    author = await author_element.inner_text() if author_element else ""

                    # Extract timestamp
                    # time_element = await post.query_selector(" time")
                    # timestamp = await time_element.get_attribute("datetime") if time_element else None
                     # Extract timestamp
                    time_element = await post.query_selector("span.tgme_widget_message_meta a.tgme_widget_message_date time")
                    if time_element:
                        timestamp = await time_element.get_attribute("datetime")
                    else:
                        # fallback: try to get inner text or attribute from other possible selectors
                        alt_time_element = await post.query_selector("span.tgme_widget_message_date")
                        if alt_time_element:
                            timestamp = await alt_time_element.get_attribute("datetime")
                            if not timestamp:
                                timestamp = await alt_time_element.inner_text()
                        else:
                            timestamp = None
                    # print (post.text_content)
                    
                        # Extract view count
                        
                        
                    views_element = await post.query_selector("span.tgme_widget_message_views")
                    views = await views_element.inner_text() if views_element else ""

                    # Extract any link
                    link_element = await post.query_selector("a.tgme_widget_message_link_preview")
                    link = await link_element.get_attribute("href") if link_element else ""

                    # message = Message(
                    #     id=message_id,
                    #     platform="telegram",
                    #     domain=task.domain,
                    #     sourcce=source.target,
                    #     created_at=timestamp,
                    #     raw_content=content,
                    #     content=content,
                    # )
                    print(timestamp)
                    content = await post.inner_text()
                    message = Message(
                        id=message_id,
                        source=source.target,
                        domain=task.domain,
                        platform="telegram",
                        raw_content=content,
                        created_at=timestamp,
                        content=content
                    )
                    batch.append(message)

                    if len(batch) >= self.batch_size:
                        yield batch
                        batch = []
                        await asyncio.sleep(self.delay)

            if batch:
                yield batch

            await browser.close()
