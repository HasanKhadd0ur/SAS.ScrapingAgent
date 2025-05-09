import json
import logging
from typing import List
from app.core.models.message import Message

logger = logging.getLogger(__name__)

class MessagesService:
    
    def publish(self, topic: str, messages: List[Message]):
        for message in messages:
            logger.debug(f"Publishing to topic {topic}: {message.content.split(" ")[0]} with {message.sentiment_label}")
            print(f"[+] Publishing to topic {topic}: {message.content.split(" ")[0]} with {message.sentiment_label}, {message.sentiment_score}")
        # print(f"[+] Publishing to topic {topic}: {messages[0].content.split(" ")[0]} with {messages[0].sentiment_label}")        
        # logger.debug(f"Publishing to topic {topic}: {messages[0].content.split(" ")[0]} with {messages[0].sentiment_label}")
        # print(f"[+] Publishing to topic {topic}: {messages[0].content.split(" ")[0]} with {messages[0].sentiment_label}")