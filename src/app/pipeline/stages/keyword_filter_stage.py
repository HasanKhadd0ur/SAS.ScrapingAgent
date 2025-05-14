from typing import Optional
from app.core.models.message import ScrapingContext
from app.pipeline.base import FilterStage

KEYWORDS = {
    "politics": ["election", "سوريا", "الشرع", "government"],
    "sports": ["goal", "match", "player", "tournament"]
}

class KeywordFilterStage(FilterStage):
    def __init__(self, keywords=KEYWORDS):
        super().__init__()
        self.keywords = keywords

    async def process(self, scraping_context : ScrapingContext, nextStep: Optional[FilterStage] = None) -> ScrapingContext:
        filtered_messages = []
        for message in scraping_context.messages:
            keywords = self.keywords.get(message.domain, [])
            content = message.content.lower()

            if any(k in content for k in keywords):
                
                filtered_messages.append(message)
        scraping_context.messages=filtered_messages
        if nextStep: 
            return await nextStep.process(scraping_context)
        return scraping_context
