# app/infrastructure/kafka_consumer.py
import json
from aiokafka import AIOKafkaConsumer
from typing import AsyncGenerator


class KafkaConsumer:
    def __init__(self, topic: str, bootstrap_servers="localhost:9092", group_id="default-group"):
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda x: json.loads(x.decode("utf-8"))
        )

    async def start(self):
        await self.consumer.start()

    async def stop(self):
        await self.consumer.stop()

    async def get_messages(self) -> AsyncGenerator[dict, None]:
        async for msg in self.consumer:
            yield msg.value
