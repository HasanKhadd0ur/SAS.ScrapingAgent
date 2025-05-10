import csv
import json
import logging
import os
from typing import List
from app.core.models.message import Message

logger = logging.getLogger(__name__)

class MessagesService:
    
    def publish(self, topic: str, messages: List[Message]):
        for message in messages:
            # logger.debug(f"Publishing to topic {topic}: {message.content.split(" ")[0]} with {message.sentiment_label}")
            print(f"[+] Publishing to topic {topic}: {message.content.split(" ")[0]} with {message.sentiment_label}, {message.sentiment_score}")
        # print(f"[+] Publishing to topic {topic}: {messages[0].content.split(" ")[0]} with {messages[0].sentiment_label}")        
        # logger.debug(f"Publishing to topic {topic}: {messages[0].content.split(" ")[0]} with {messages[0].sentiment_label}")
        # print(f"[+] Publishing to topic {topic}: {messages[0].content.split(" ")[0]} with {messages[0].sentiment_label}")
        
    def save_messages(self,messages : List[Message],file_path :str):
          self._ensure_file_has_headers(file_path)
          with open(file_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for msg in messages:
                writer.writerow([
                    msg.timestamp,
                    msg.domain,
                    msg.channel,
                    msg.source,
                    msg.content,
                    msg.raw_content,
                    getattr(msg, "sentiment_score", ""),
                    getattr(msg, "sentiment_label", "")
                ])
    
    def _ensure_file_has_headers(self,file_path :str):
        if not os.path.exists(file_path):
            with open(file_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "source", "domain","channel","content", "raw_content", "sentiment_score", "sentiment_label"])
