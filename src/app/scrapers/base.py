from abc import ABC, abstractmethod
from app.core.models.message import Message
from app.core.models.scraper_task import ScrapingTask
from typing import List

class BaseScraper(ABC):
    def __init__(self, config :dict):
        self.config = config

    @abstractmethod
    async def run_task(self, task: ScrapingTask) -> List[Message]:
        pass
