import csv
import json
import logging
import os
from typing import List
from app.core.models.message import Message
from app.kafka.kafka_producer import KafkaProducer

logger = logging.getLogger(__name__)

class MessagesService:
    
    # def __init__(self):
    #     # self.kafka_producer = kafka_producer

 
    async def publish(self, topic: str, messages: List[Message]):
        
        # Prepare all messages in the batch dynamically using the message attributes
        payloads = [self._serialize_message(message) for message in messages]

        # Send all messages at once
        self.kafka_producer.send(topic, payloads)
        
        # Log and print a summary of the batch publication
        logger.info(f"Published batch to topic '{topic}': {len(messages)} messages")
        print(f"[+] Published batch to topic {topic}: {len(messages)} messages")
        
        # Optionally log the details of the first message in the batch (for debugging purposes)
        if messages:
            logger.debug(f"First message in batch: '{messages[0].content[:20]}...' with label={messages[0].sentiment_label}, score={messages[0].sentiment_score}")
            print(f"[+] First message in batch: '{messages[0].content[:20]}...' with label={messages[0].sentiment_label}, score={messages[0].sentiment_score}")
            # logger.debug(f"Publishing to topic {topic}: {message.content.split(" ")[0]} with {message.sentiment_label}")
            # print(f"[+] Publishing to topic {topic}: {message.content.split(" ")[0]} with {message.sentiment_label}, {message.sentiment_score}")
    
    def _serialize_message(self, message: Message) -> dict:
        """
        Serializes a Message object into a dictionary for publishing.
        This method can be modified to handle any additional attributes dynamically.
        """
        # return  json.dumps(message).encode('utf-8')
        return {
            "id": message.id,
            "content": message.content,
            "sentiment_label": message.sentiment_label,
            "sentiment_score": message.sentiment_score,
            "created_at": message.created_at,  
            "platform":message.platform,
            "source":message.source,
            "raw_content":message.raw_content
        }
        
    def save_messages(self,messages : List[Message],file_path :str):
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
    
    def _ensure_file_has_headers(self,file_path :str):
        if not os.path.exists(file_path):
            with open(file_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "domain","platform", "source","content", "raw_content", "sentiment_score", "sentiment_label"])
    def set_kafka_producer(self,kafka_producer : KafkaProducer):
        self.kafka_producer=kafka_producer