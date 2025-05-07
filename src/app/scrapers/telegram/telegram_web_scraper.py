from app.scrapers.base import BaseScraper
from app.core.models.scraper_task import ScraperTask
from app.core.models.message import Message
from typing import List
from playwright.async_api import async_playwright
import asyncio

class TelegramWebScraper(BaseScraper):
    
    async def run_task(self, task: ScraperTask) -> List[Message]:
        messages = []

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            for source in task.sources:
                channel_url = f"https://t.me/s/{source.target}"

                await page.goto(channel_url)
                await page.wait_for_timeout(2000)  # let it load a bit

                posts = await page.query_selector_all("div.tgme_widget_message_text")
                for post in posts[-task.limit:]:
                    content = await post.inner_text()
                    messages.append(Message(
                        source="telegram",
                        domain=task.domain,
                        channel=source.target,
                        base_content=content,
                        content=content,
                    ))

            await browser.close()

        return messages
