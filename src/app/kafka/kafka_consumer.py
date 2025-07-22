import json
from aiokafka import AIOKafkaConsumer
from typing import AsyncGenerator


class KafkaConsumer:
    def __init__(self, 
            topic: str, 
            bootstrap_servers="localhost:9092", 
            group_id="default-group",
            group_instance_id: str = None,
            auto_offset_reset='earliest'):

        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            group_instance_id=group_instance_id,  # 🧠 key addition
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            heartbeat_interval_ms=3000,     
            session_timeout_ms=30000,       
            max_poll_interval_ms=600000,
            auto_offset_reset=auto_offset_reset,#"earliest",  # Or "latest" depending on your needs
            enable_auto_commit=True
        )

    async def start(self):
        await self.consumer.start()

    async def stop(self):
        await self.consumer.stop()

    async def get_messages(self) -> AsyncGenerator[dict, None]:
        async for msg in self.consumer:
            yield msg.value
