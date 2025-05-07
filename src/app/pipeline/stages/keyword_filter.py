
from app.core.models.message import Message
from app.pipeline.base import FilterStage


KEYWORDS = {
    "politics": ["election", "president", "policy", "government"],
    "sports": ["goal", "match", "player", "tournament"]
}

class KeywordFilter(FilterStage):
  
    def __init__(self, keywords= KEYWORDS):
        super().__init__()
        self.keywords=keywords


    def process(self, message: Message , nextStep: FilterStage = None):
        # Filter logic for keywords based on domain
        keywords = self.keywords.get(message.domain, [])
        content = message.content.lower()

        # If no keywords are found, discard the message
        if not any(k in content for k in keywords):
            return None

        # If there's a next step, delegate the message
        if nextStep:
            return nextStep.process(message)
        return message
