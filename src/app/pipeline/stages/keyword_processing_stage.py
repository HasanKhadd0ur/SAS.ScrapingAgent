import re
import httpx
from typing import Optional
from app.core.models.message import ScrapingContext
from app.pipeline.base.processing_stage import ProcessingStage
from app.core.configs.base_config import BaseConfig

class KeywordProcessingStage(ProcessingStage):
    def __init__(self, config: BaseConfig):
        super().__init__()
        self.config = config
        self.keywords_url = config.get_master_url() + '/api/BlockedTerms'
        self.keywords: list[str] = None

    def normalize(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"ـ{3,}.*$", "", text)
        text = re.sub(r"http\S+$", "", text)
        text = re.sub(r"[^\w\s]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    async def load_keywords(self):
        try:
            async with httpx.AsyncClient(verify=False) as client:
                response = await client.get(self.keywords_url)
                if response.status_code == 200:
                    raw_keywords = [k['term'] for k in response.json()]
                    self.keywords = [self.normalize(k) for k in raw_keywords]
                    print(f"[INFO] Loaded {len(self.keywords)} normalized blocked keywords from server.")
                else:
                    print(f"[ERROR] Failed to load keywords. Status: {response.status_code}")
        except Exception as e:
            print(f"[ERROR] Exception while fetching keywords: {e}")

    async def process(self, scraping_context: ScrapingContext, nextStep: Optional[ProcessingStage] = None) -> ScrapingContext:
        if self.keywords is None:
            await self.load_keywords()

        allowed_messages = []
        for message in scraping_context.messages:
            normalized_content = self.normalize(message.content)
            if not any(term in normalized_content for term in self.keywords):
                allowed_messages.append(message)

        scraping_context.messages = allowed_messages

        if nextStep:
            return await nextStep.process(scraping_context)
        return scraping_context
