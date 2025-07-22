class MockKafkaPublisher:
    def __init__(self):
        self.published_messages = []

    async def publish(self, message: dict, topic: str):
        self.published_messages.append((topic, message))
        # Simulate a slight delay if desired
        await asyncio.sleep(0.001)