from typing import Optional
from app.core.models.message import ScrapingContext
from app.core.services.messages_service import MessagesService
from app.pipeline.base import FilterStage

class MessagesSavingStage(FilterStage):
    def __init__(self, file_path: str = "..//assets//messages.csv"):
        super().__init__()
        self.file_path = file_path

    async def process(self, scraping_context : ScrapingContext, nextStep: Optional[FilterStage] = None) -> ScrapingContext:
        messages_service = MessagesService()
        messages_service.save_messages(scraping_context.messages,self.file_path)
        if nextStep:
            return await nextStep.process(scraping_context.messages)
        return scraping_context
