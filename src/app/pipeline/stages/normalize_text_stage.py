from typing import List, Optional
from app.core.models.message import Message
from app.pipeline.base import FilterStage
import re

class NormalizeTextStage(FilterStage):
 
    def normalize(self, text: str) -> str:
        # Basic normalization: lowercase, remove extra spaces, strip punctuation
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text)  # remove punctuation
        text = re.sub(r"\s+", " ", text).strip()  # normalize spaces
        return text

    def process(self, messages: List[Message], nextStep: Optional[FilterStage] = None) -> List[Message]:
        for message in messages:
            message.content = self.normalize(message.content)
            message.base_content = self.normalize(message.base_content)

        if nextStep:
            return nextStep.process(messages)
        return messages
