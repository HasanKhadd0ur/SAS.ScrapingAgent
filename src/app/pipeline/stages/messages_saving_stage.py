import csv
from typing import List, Optional
from app.core.models.message import Message
from app.core.services.messages_service import MessagesService
from app.pipeline.base import FilterStage
import os

class MessagesSavingStage(FilterStage):
    def __init__(self, file_path: str = "..//assets//messages.csv"):
        super().__init__()
        self.file_path = file_path

    def process(self, messages: List[Message], nextStep: Optional[FilterStage] = None) -> List[Message]:
        messagesService = MessagesService()
        messagesService.save_messages(messages,self.file_path)
        if nextStep:
            return nextStep.process(messages)
        return messages
