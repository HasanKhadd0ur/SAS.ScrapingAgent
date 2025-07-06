from typing import  Optional
from app.core.models.message import ScrapingContext
from app.pipeline.base import FilterStage
import re

class NormalizeTextStage(FilterStage):
 
    def normalize(self, text: str) -> str:
        # Basic normalization: lowercase, remove extra spaces, strip punctuation
        text = text.lower()
        # Remove everything after three or more Tatweel characters
        text = re.sub(r"ـ{3,}.*$", "", text)
        # Also remove trailing junk strings like 'httpstmemq_qu' (assumed no spaces)
        text = re.sub(r"http\S+$", "", text)

        
        text = re.sub(r"[^\w\s]", "", text)  # remove punctuation
        text = re.sub(r"\s+", " ", text).strip()  # normalize spaces
        return text

    async def process(self, scraping_context : ScrapingContext, nextStep: Optional[FilterStage] = None) -> ScrapingContext:
        for message in scraping_context.messages:
            message.content = self.normalize(message.content)

        if nextStep:
            return await nextStep.process(scraping_context)
        return scraping_context
