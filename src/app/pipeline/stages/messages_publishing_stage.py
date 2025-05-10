from typing import List, Optional
from app.core.models.message import Message
from app.core.services.logging_service import LoggingService
from app.pipeline.base import FilterStage
from app.core.services.messages_service import MessagesService

logger = LoggingService("MessagesPublishingStage").get_logger()

class MessagesPublishingStage(FilterStage):
    def __init__(self):
        super().__init__()
        self.messagesService = MessagesService()

    def process(self, messages: List[Message], nextStep: Optional[FilterStage] = None) -> List[Message]:
        for message in messages:
            try:
                self.messagesService.publish(message.domain, [message])  # Convert to dict if needed
            except Exception as e:
                logger.exception(f"Failed to publish message ID")
        if nextStep:
            return nextStep.process(messages)
        return messages
