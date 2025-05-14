import json
from kafka import KafkaProducer as SyncKafkaProducer

class KafkaProducer:
    def __init__(self, bootstrap_servers="localhost:9092"):
        # Use the synchronous KafkaProducer from kafka-python
        self.producer = SyncKafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

    def send(self, topic: str, value: dict):
        # Synchronously send a message to the Kafka topic
        self.producer.send(topic, value)
        # Ensure the message is written to Kafka
        self.producer.flush()

    def stop(self):
        # Close the producer when done
        self.producer.close()
