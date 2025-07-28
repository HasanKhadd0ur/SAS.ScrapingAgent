from time import sleep
from app.core.configs.base_config import BaseConfig
from app.scrapers.base.base_scraper import BaseScraper
from app.core.models.scraper_task import ScrapingTask
from app.core.models.message import Message
from typing import AsyncGenerator, List
from playwright.async_api import async_playwright
import asyncio
from random import randint


class TelegramWebScraper(BaseScraper):
    def __init__(self, config_service: BaseConfig):
        config=config_service.get_config("TELEGRAM_WEB_SCRAPER_CONFIG")
        self.batch_size = 30 #config.get("batch_size", 5)
        self.delay = config.get("delay", 0.1)
        self.selector = config.get("selector", "div.tgme_widget_message")

    async def run_task(self, task: ScrapingTask) -> AsyncGenerator[List[Message], None]:
        batch = []

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            for source in task.sources:
                channel_url = f"https://t.me/s/{source.target}"

                await page.goto(channel_url)
                await page.wait_for_timeout(int(self.delay * 1000)+ randint(1000,10000))  # convert to ms

                await page.wait_for_timeout(randint(500, 1500)) # Small additional delay after selector wait

                posts = await page.query_selector_all(self.selector)
                
                
                for post in posts[-source.limit:]:
                    # sleep(10)
                    # Extract message ID
                    data_post = await post.get_attribute("data-post")
                    message_id = data_post.split("/")[-1] if data_post else None

                    # Channel name
                    # channel_tag = await post.query_selector(".tgme_widget_message_author a.tgme_widget_message_owner_name span")
                    # channel_name = await channel_tag.inner_text() if channel_tag else source.target

                    # Message text
                    text_tag = await post.query_selector(".tgme_widget_message_text")
                    text = await text_tag.inner_text() if text_tag else ""

                    # Link preview (if exists)
                    link_preview = await post.query_selector(".tgme_widget_message_link_preview")
                    preview_link = await link_preview.get_attribute("href") if link_preview else ""
                    preview_title = ""
                    preview_description = ""
                    preview_image = ""

                    if link_preview:
                        title_elem = await link_preview.query_selector(".link_preview_title")
                        desc_elem = await link_preview.query_selector(".link_preview_description")
                        image_elem = await link_preview.query_selector(".link_preview_image")

                        preview_title = await title_elem.inner_text() if title_elem else ""
                        preview_description = await desc_elem.inner_text() if desc_elem else ""

                        if image_elem:
                            style = await image_elem.get_attribute("style")
                            if style and "url('" in style:
                                start = style.find("url('") + 5
                                end = style.find("')", start)
                                preview_image = style[start:end]

                    # Views
                    views_tag = await post.query_selector(".tgme_widget_message_views")
                    views = await views_tag.inner_text() if views_tag else ""

                    # Timestamp
                    await page.wait_for_selector(".tgme_widget_message_date time", timeout=5000)
                    time_tag = await post.query_selector(".tgme_widget_message_date time")
                    # print(time_tag.inner_text)
                    timestamp = await time_tag.get_attribute("datetime") if time_tag else None

                    # Service date (optional)
                    service_date_tag = await post.query_selector(".tgme_widget_message_service_date")
                    service_date = await service_date_tag.inner_text() if service_date_tag else ""

                    # Raw content
                    # raw_content = await post.inner_text()
                    # print(timestamp)
                    # message = Message(
                    #     id=message_id,
                    #     platform="telegram",
                    #     domain=task.domain,
                    #     sourcce=source.target,
                    #     created_at=timestamp,
                    #     raw_content=content,
                    #     content=content,
                    # )
                    # print(timestamp)
                    content = await post.inner_text()
                    message = Message(
                        id=message_id,
                        source=source.target,
                        domain=task.domain,
                        platform="telegram",
                        raw_content=content,
                        created_at=timestamp,
                        content=content,
                        metadata={
                            "preview_link": preview_link,
                            "preview_title": preview_title,
                            "preview_description": preview_description,
                            "preview_image": preview_image,
                            "views": views,
                            "service_date": service_date,
                        }
                    )
                    batch.append(message)

                    if len(batch) >= self.batch_size:
                        yield batch
                        batch = []
                        await asyncio.sleep(self.delay)

            if batch:
                yield batch

            await browser.close()
