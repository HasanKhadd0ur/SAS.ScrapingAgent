from abc import ABC, abstractmethod
from app.core.models.message import Message
from app.core.models.scraper_task import ScraperTask
from typing import List

class BaseScraper(ABC):
    def __init__(self, credentials: dict):
        self.credentials = credentials

    @abstractmethod
    async def run_task(self, task: ScraperTask) -> List[Message]:
        pass
