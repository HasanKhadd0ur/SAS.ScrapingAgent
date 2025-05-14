from typing import  Optional
from app.core.models.message import ScrapingContext
from app.pipeline.base import FilterStage
import re

class NormalizeTextStage(FilterStage):
 
    def normalize(self, text: str) -> str:
        # Basic normalization: lowercase, remove extra spaces, strip punctuation
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text)  # remove punctuation
        text = re.sub(r"\s+", " ", text).strip()  # normalize spaces
        return text

    async def process(self, scraping_context : ScrapingContext, nextStep: Optional[FilterStage] = None) -> ScrapingContext:
        for message in scraping_context.messages:
            message.content = self.normalize(message.content)

        if nextStep:
            return await nextStep.process(scraping_context)
        return scraping_context
