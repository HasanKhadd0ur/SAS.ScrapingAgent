from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
    id:str=""
    source: str=""
    domain: str=""
    channel: str=""
    base_content: str=""
    content: str=""
    timestamp: datetime = datetime.utcnow()
    metadata: dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
