from typing import Dict, Any

class FeedbackService:
    def __init__(self, kafka_producer, topic: str):
        self.producer = kafka_producer
        self.topic = topic

    async def send_feedback(self, feedback_data: Dict[str, Any]):
        await self.producer.send(self.topic, feedback_data)
