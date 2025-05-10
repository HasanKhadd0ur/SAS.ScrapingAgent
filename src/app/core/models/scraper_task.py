from dataclasses import dataclass
from typing import List


@dataclass
class DataSource:
    target: str
    config: dict = None
    limit: int =1 
@dataclass
class ScrapingApproach:
    mode: str ="web"
    name: str="dummy"
    
@dataclass
class ScrapingTask:
    id: str
    domain: str
    sources: List[DataSource]
    limit: int = 5
    scraping_approach: ScrapingApproach =ScrapingApproach()

