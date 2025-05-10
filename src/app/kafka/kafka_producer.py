# app/infrastructure/kafka_producer.py
import json
from aiokafka import AIOKafkaProducer


class KafkaProducer:
    def __init__(self, bootstrap_servers="localhost:9092"):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send(self, topic: str, value: dict):
        await self.producer.send_and_wait(topic, value)
