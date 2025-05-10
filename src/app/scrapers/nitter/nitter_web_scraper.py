from app.scrapers.base import BaseScraper
from app.core.models.scraper_task import ScraperTask
from app.core.models.message import Message

from typing import List
from playwright.async_api import async_playwright


class NitterWebScraper(BaseScraper):

    async def run_task(self, task: ScraperTask) -> List[Message]:
        messages = []

        query = task.sources[0].target.replace(" ", "+")
        search_url = f"https://lightbrd.com/search?f=tweets&q={query}"

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            print(f"Searching Nitter for query: {query}")
            
            try:
                await page.goto(search_url, timeout=10000)
                await page.screenshot(path="nitter_debug.png")

                await page.wait_for_selector("div.timeline-item", timeout=5000)

                while len(messages) < task.limit:
                    tweet_elements = await page.query_selector_all("div.timeline-item")

                    for tweet in tweet_elements:
                        if len(messages) >= task.limit:
                            break

                        try:
                            username_el = await tweet.query_selector("a.username")
                            tweet_text_el = await tweet.query_selector("div.tweet-content")
                            time_el = await tweet.query_selector("span.tweet-date a")

                            if username_el and tweet_text_el and time_el:
                                username = await username_el.inner_text()
                                tweet_text = await tweet_text_el.inner_text()
                                tweet_time = await time_el.get_attribute("title")

                                messages.append(Message(
                                    source="nitter",
                                    domain=task.domain,
                                    channel=username,
                                    raw_content=tweet_text,
                                    content=tweet_text
                                ))
                        except Exception as e:
                            print(f"[Tweet Parse Error] {e}")
                            continue

                    # Try to click "Load more" if it exists
                    try:
                        load_more_button = await page.query_selector("div.show-more")
                        if load_more_button:
                            await load_more_button.click()
                            await page.wait_for_timeout(2000)
                        else:
                            break  # No more tweets
                    except Exception:
                        break

            except Exception as e:
                print(f"[Error while scraping] {e}")
            finally:
                await browser.close()

        return messages
