from dataclasses import dataclass
from typing import List


@dataclass
class DataSource:
    target: str
    limit: int =1 

    # config: dict = None

@dataclass
class ScrapingApproach:
    mode: str ="Dummy"
    platform:str ="File"
    name: str="DummyFileScraper"
    
@dataclass
class ScrapingTask:
    id: str
    domain: str
    platform:str
    sources: List[DataSource]
    limit: int = 5
    scraping_approach: ScrapingApproach =ScrapingApproach

