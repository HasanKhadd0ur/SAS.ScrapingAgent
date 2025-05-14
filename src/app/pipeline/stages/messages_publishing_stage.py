from typing import Optional
from app.core.models.message import ScrapingContext
from app.core.services.logging_service import LoggingService
from app.pipeline.base import FilterStage
from app.core.services.messages_service import MessagesService
from app.kafka.kafka_producer import KafkaProducer

logger = LoggingService("MessagesPublishingStage").get_logger()

class MessagesPublishingStage(FilterStage):
    def __init__(self):
        super().__init__()
        self.messagesService = MessagesService()
        self.messagesService.set_kafka_producer(KafkaProducer())

    async def process(self,scraping_context : ScrapingContext, nextStep: Optional[FilterStage] = None) -> ScrapingContext:
        try:
            await self.messagesService.publish(scraping_context.task.platform +scraping_context.task.domain, scraping_context.messages)
        except Exception as _:
            logger.exception(f"Failed to publish messages ")
            
        if nextStep:
            return await nextStep.process(scraping_context)
        return scraping_context
