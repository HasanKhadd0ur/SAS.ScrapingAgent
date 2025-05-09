from typing import List, Optional
from app.core.models.message import Message
from app.pipeline.base import FilterStage

KEYWORDS = {
    "politics": ["election", "سوريا", "الشرع", "government"],
    "sports": ["goal", "match", "player", "tournament"]
}

class KeywordFilterStage(FilterStage):
    def __init__(self, keywords=KEYWORDS):
        super().__init__()
        self.keywords = keywords

    def process(self, messages: List[Message], nextStep: Optional[FilterStage] = None) -> List[Message]:
        filtered_messages = []
        for message in messages:
            keywords = self.keywords.get(message.domain, [])
            content = message.content.lower()

            if any(k in content for k in keywords):
                if nextStep:
                    next_result = nextStep.process([message])
                    if next_result:
                        filtered_messages.extend(next_result)
                else:
                    filtered_messages.append(message)

        return filtered_messages
