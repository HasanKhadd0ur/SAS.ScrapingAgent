from dataclasses import dataclass
from datetime import datetime
from typing import List

from app.core.models.scraper_task import ScrapingTask

@dataclass
class Message:
    id:str=""
    source: str=""
    domain: str=""
    platform: str=""
    raw_content: str=""
    content: str=""
    sentiment_label: str=""
    sentiment_score: float =0
    timestamp: datetime = datetime.utcnow()
    metadata: dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

@dataclass
class PipelineContext:
    pass

@dataclass
class ScrapingContext(PipelineContext): 
    messages: List[Message]
    task:ScrapingTask=None
    metadata: dict = None
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
