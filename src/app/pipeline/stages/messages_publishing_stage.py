import asyncio
from typing import List, Optional
from app.core.models.message import Message
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

    async def process(self, messages: List[Message], nextStep: Optional[FilterStage] = None) -> List[Message]:
        try:
            await self.messagesService.publish(messages[0].domain, messages)
        except Exception as e:
            logger.exception(f"Failed to publish messages ")
        if nextStep:
            return await nextStep.process(messages)
        return messages
