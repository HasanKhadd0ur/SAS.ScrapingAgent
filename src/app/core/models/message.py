from dataclasses import dataclass
from datetime import datetime

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
class MessageContext: 
    message: Message 