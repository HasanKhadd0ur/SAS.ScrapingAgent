import pytest
import time
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from unittest.mock import patch, MagicMock
import random
import warnings

from app.agent import Agent
from app.scrapers.sources.dummy.dummy_file_scrarper import DummyFileScraper
from app.pipeline.factory.default_pipelines import preprocessing_pipeline, publishing_pipeline
from app.core.configs.env_config import EnvConfig

warnings.filterwarnings("ignore")


from app.core.models.scraper_task import ScrapingApproach


class MockTask:
    def __init__(self, id, scraping_approach= ScrapingApproach(),limit=100):
        self.id = id
        self.scraping_approach :ScrapingApproach = scraping_approach
        self.domain='Politics'
        self.platform='Telegram'
        self.limit=limit


class MockTasksService:
    def __init__(self, limit):
        self.limit = limit

    async def stream_tasks(self):
        for i in range(self.limit):
            yield MockTask(id=f"task-{i}",limit=self.limit)

    async def assign_executor(self, scraper_id, scraping_task_id):
        pass

    async def complete_task(self, task_id):
        pass




@patch("app.pipeline.stages.messages_publishing_stage.KafkaProducer")
@pytest.mark.asyncio
async def test_stream_throughput(mock_kafka_producer):
    # Configuration
    NUM_BURSTS = 4
    MESSAGES_PER_BURST = [random.randint(100, 200) for _ in range(NUM_BURSTS)]
    MIN_MSGS_PER_SEC = 1.5  # realistic minimum threshold (100 per minute)
    
    # Mock Kafka producer
    mock_producer_instance = MagicMock()
    mock_producer_instance.send.return_value = None
    mock_kafka_producer.return_value = mock_producer_instance

    dummy_scraper = DummyFileScraper(config_service=EnvConfig())
    agent = Agent(
        scraper=dummy_scraper,
        preprocessing_pipeline=preprocessing_pipeline,
        publishing_pipeline=publishing_pipeline
    )

    burst_durations = []
    burst_throughputs = []
    burst_msg_counts = []

    total_msgs = 0
    print("\nBenchmarking 4 bursts (100–300 messages per burst):")

    for i, num_msgs in enumerate(MESSAGES_PER_BURST):
        print(f"\nBurst {i + 1}: {num_msgs} messages")
        
        tasks_service = MockTasksService(num_msgs)
        processed_messages = 0
        start = time.time()

        async for task in tasks_service.stream_tasks():
            agent.set_scraper(dummy_scraper)
            agent.assign_task(task)
            processed = await agent.run()
            await tasks_service.complete_task(task.id)
            processed_messages += processed

        duration = time.time() - start
        throughput = processed_messages / duration

        burst_durations.append(duration)
        burst_throughputs.append(throughput)
        burst_msg_counts.append(processed_messages)
        total_msgs += processed_messages

        print(f"Processed {processed_messages} messages in {duration:.2f}s -> {throughput:.2f} msgs/sec")
        assert throughput >= MIN_MSGS_PER_SEC, f"Burst {i + 1} throughput too low"

    # Save results
    os.makedirs("benchmark_results", exist_ok=True)
    bursts = np.arange(1, NUM_BURSTS + 1)

    # Plot 1: Time per burst
    plt.figure(figsize=(10, 6))
    plt.plot(bursts, burst_durations, marker='o', label='Time per Burst (s)', color='orange')
    plt.xlabel("Burst")
    plt.ylabel("Time (seconds)")
    plt.title("Time per Burst")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("benchmark_results/time_per_burst.png")

    # Plot 2: Messages per burst
    plt.figure(figsize=(10, 6))
    plt.bar(bursts, burst_msg_counts, label='Messages Processed')
    plt.xlabel("Burst")
    plt.ylabel("Messages")
    plt.title("Messages Processed per Burst")
    plt.grid(axis='y')
    plt.legend()
    plt.tight_layout()
    plt.savefig("benchmark_results/messages_per_burst.png")

    # Plot 3: Throughput
    plt.figure(figsize=(10, 6))
    plt.plot(bursts, burst_throughputs, marker='x', label='Throughput (msgs/sec)', color='green')
    plt.xlabel("Burst")
    plt.ylabel("Throughput")
    plt.title("Throughput per Burst")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("benchmark_results/throughput_per_burst.png")

    # CSV stats
    stats_df = pd.DataFrame({
        "burst": bursts,
        "messages_processed": burst_msg_counts,
        "time_seconds": burst_durations,
        "throughput_msgs_per_sec": burst_throughputs
    })
    stats_df.to_csv("benchmark_results/stream_benchmark_stats.csv", index=False)

    print(f"\n✅ Total messages processed: {total_msgs}")
