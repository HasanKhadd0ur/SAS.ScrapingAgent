from dataclasses import dataclass
from typing import List


@dataclass
class ScraperSource:
    target: str
    config: dict = None

@dataclass
class ScraperTask:
    domain: str
    sources: List[ScraperSource]
    limit: int = 5