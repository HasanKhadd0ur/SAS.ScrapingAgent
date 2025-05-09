from dataclasses import dataclass
from typing import List


@dataclass
class ScraperSource:
    target: str
    config: dict = None
    limit: int =1 

@dataclass
class ScraperTask:
    id: str
    domain: str
    sources: List[ScraperSource]
    limit: int = 5