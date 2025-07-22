from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

import numpy as np

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
    created_at: datetime = datetime.utcnow()
    embedding: Optional[List[float]] = None
    metadata: dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "source": self.source,
            "domain": self.domain,
            "platform": self.platform,
            "raw_content": self.raw_content,
            "content": self.content,
            "sentiment_label": self.sentiment_label,
            "sentiment_score": self.sentiment_score,
            "created_at":  self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            "embedding": self.embedding.tolist() if isinstance(self.embedding, np.ndarray) else self.embedding,
            "metadata": self.metadata
        }

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
