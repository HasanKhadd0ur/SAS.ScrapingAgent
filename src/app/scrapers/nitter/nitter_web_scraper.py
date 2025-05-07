from app.scrapers.base import BaseScraper
from app.core.models.scraper_task import ScraperTask
from app.core.models.message import Message



from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class HTML:
    search_field = '//*[@id="search"]'
    search_button = '/html/body/div/div/div[1]/form/button'
    load_more_button = '//div[contains(@class,"show-more")]'
    tweet_container = 'timeline-item'
    tweet_username = 'username'
    tweet_text = 'tweet-content'
    tweet_time = 'tweet-date'

def start_webdriver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=chrome_options)


class NitterWebScraper(BaseScraper):

    def run_task(self, task: ScraperTask) -> List[Message]:
        driver = start_webdriver()
        html = HTML()

        messages = []
        try:
            query = task.target
            driver.get("https://nitter.poast.org/search?")
            print(f"Searching Nitter for query: {query}")

            # Enter query
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, html.search_field))
            ).send_keys(query)

            # Click search button
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, html.search_button))
            ).click()

            while len(messages) < task.limit:
                # Wait for content to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, html.load_more_button))
                )

                soup = BeautifulSoup(driver.page_source, 'html.parser')
                tweets = soup.find_all('div', class_=html.tweet_container)

                for tweet in tweets:
                    if len(messages) >= task.limit:
                        break

                    try:
                        username = tweet.find('a', class_=html.tweet_username).get_text()
                        tweet_text = tweet.find('div', class_=html.tweet_text).get_text()
                        tweet_time = tweet.find('span', class_=html.tweet_time).find('a')['title']

                        messages.append(Message(
                            source="nitter",
                            domain=task.domain,
                            channel=username,
                            base_content=tweet_text,
                            content=tweet_text,
                        ))

                    except AttributeError:
                        continue

                # Click load more
                driver.find_element(By.XPATH, html.load_more_button).click()

        except Exception as e:
            print(f"[Error] {e}")
        finally:
            driver.quit()

        return messages

# from app.scrapers.base import BaseScraper
# from app.core.models.scraper_task import ScraperTask
# from app.core.models.message import Message
# from typing import List
# from playwright.async_api import async_playwright

# class NitterWebScraper(BaseScraper):
#     async def run_task(self, task: ScraperTask) -> List[Message]:
#         messages = []

#         async with async_playwright() as p:
#             browser = await p.chromium.launch(headless=True)
#             page = await browser.new_page()

#             query = task.sources[0].target.replace(" ", "+")
#             search_url = f"https://nitter.net/search?f=tweets&q={query}"
#             await page.wait_for_timeout(2000)
#             await page.goto(search_url)
#             await page.wait_for_selector("div.timeline-item", timeout=5000)

#             tweets = await page.query_selector_all("div.timeline-item")

#             for tweet in tweets[:task.limit]:
#                 content_node = await tweet.query_selector("div.tweet-content")
#                 if content_node:
#                     content = await content_node.inner_text()
#                     messages.append(Message(
#                         source="nitter",
#                         domain=task.domain,
#                         channel="search",
#                         base_content=content,
#                         content=content,
#                     ))

#             await browser.close()

#         return messages
