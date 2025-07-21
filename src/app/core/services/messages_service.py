import csv
import json
import logging
import os
from typing import List
from app.core.models.message import Message
from app.kafka.kafka_producer import KafkaProducer

logger = logging.getLogger(__name__)

class MessagesService:

    async def publish(self, topic: str, messages: List[Message]):
        try:
            payloads = [self._serialize_message(message) for message in messages]
            
            # Send all messages at once
            self.kafka_producer.send(topic, payloads)
            
            # Log and print a summary of the batch publication
            logger.info(f"Published batch to topic '{topic}': {len(messages)} messages")
            print(f"[INFO] Published batch to topic {topic}: {len(messages)} messages")
            
            if messages:
                logger.debug(f"First message in batch: '{messages[0].content[:20]}...' with label={messages[0].sentiment_label}, score={messages[0].sentiment_score}")
                print(f"[INFO] First message in batch: '{messages[0].content[:20]}...' with label={messages[0].sentiment_label}, score={messages[0].sentiment_score}")
        
        except Exception as e:
            logger.error(f"Failed to publish messages to topic '{topic}': {str(e)}", exc_info=True)
            print(f"[ERROR] Failed to publish messages to topic '{topic}': {str(e)}")

    def _serialize_message(self, message: Message) -> dict:
        return {
            "id": message.id,
            "content": message.content,
            "sentiment_label": message.sentiment_label,
            "sentiment_score": message.sentiment_score,
            "created_at": message.created_at,  
            "platform": message.platform,
            "source": message.source,
            "raw_content": message.raw_content
        }
        
    def save_messages(self, messages: List[Message], file_path: str):
        try:
            self._ensure_file_has_headers(file_path)
            with open(file_path, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                for msg in messages:
                    writer.writerow([
                        msg.created_at,
                        msg.domain,
                        msg.platform,
                        msg.source,
                        msg.content,
                        msg.raw_content,
                        getattr(msg, "sentiment_score", ""),
                        getattr(msg, "sentiment_label", "")
                    ])
        except Exception as e:
            logger.error(f"Failed to save messages to file '{file_path}': {str(e)}", exc_info=True)
            print(f"[ERROR] Failed to save messages to file '{file_path}': {str(e)}")

    def _ensure_file_has_headers(self, file_path: str):
        if not os.path.exists(file_path):
            with open(file_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "domain", "platform", "source", "content", "raw_content", "sentiment_score", "sentiment_label"])

    def set_kafka_producer(self, kafka_producer: KafkaProducer):
        self.kafka_producer = kafka_producer
