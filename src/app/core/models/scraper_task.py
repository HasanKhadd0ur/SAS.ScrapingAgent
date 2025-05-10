from dataclasses import dataclass
from typing import List


@dataclass
class DataSource:
    target: str
    config: dict = None
    limit: int =1 
@dataclass
class ScrapingApproach:
    mode: str ="Dummy"
    platform:str ="File"
    name: str="DummyFileScraper"
    
@dataclass
class ScrapingTask:
    id: str
    domain: str
    sources: List[DataSource]
    limit: int = 5
    scraping_approach: ScrapingApproach =ScrapingApproach

