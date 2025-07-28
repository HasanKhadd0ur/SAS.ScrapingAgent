import pytest
import time
from unittest.mock import patch, MagicMock
import matplotlib.pyplot as plt
import numpy as np
import os

from app.agent import Agent
from app.scrapers.sources.dummy.dummy_file_scrarper import DummyFileScraper
from tests.mocks.mock_test import MockTasksService
from app.pipeline.factory.default_pipelines import preprocessing_pipeline, publishing_pipeline
from app.core.configs.env_config import EnvConfig
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message="Trying to unpickle estimator.*")  # for sklearn


# Patch the KafkaProducer where it's used in MessagesPublishingStage
@patch("app.pipeline.stages.messages_publishing_stage.KafkaProducer")
@pytest.mark.asyncio
async def test_throughput_with_mocked_kafka(mock_kafka_producer):
    NUM_TASKS = 100
    MIN_THROUGHPUT = 0.001  # tasks/sec

    # Mock Kafka producer
    mock_producer_instance = MagicMock()
    mock_producer_instance.send.return_value = None
    mock_kafka_producer.return_value = mock_producer_instance

    tasks_service = MockTasksService(NUM_TASKS)
    dummy_scraper = DummyFileScraper(config_service=EnvConfig())

    agent = Agent(
        scraper=dummy_scraper,
        preprocessing_pipeline=preprocessing_pipeline,
        publishing_pipeline=publishing_pipeline
    )

    per_task_times = []
    per_task_messages = []

    count = 0
    total_messages = 0
    start_total = time.time()

    async for task in tasks_service.stream_tasks():
        agent.set_scraper(dummy_scraper)
        agent.assign_task(task)

        start_task = time.time()
        processed = await agent.run()
        end_task = time.time()

        await tasks_service.complete_task(task.id)

        per_task_times.append(end_task - start_task)
        per_task_messages.append(processed)
        total_messages += processed
        count += 1

    elapsed_total = time.time() - start_total
    throughput = count / elapsed_total

    print(f"\nProcessed {count} tasks in {elapsed_total:.2f}s.")
    print(f"Total messages processed: {total_messages}")
    print(f"Throughput = {throughput:.2f} tasks/sec")

    # Save plot
    os.makedirs("benchmark_results", exist_ok=True)
    task_indices = np.arange(1, count + 1)

    plt.figure(figsize=(10, 6))
    plt.plot(task_indices, per_task_messages, marker='o', label="Messages per Task")
    plt.xlabel("Task Index")
    plt.ylabel("Messages Processed")
    plt.title("Messages Processed per Task")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("benchmark_results/messages_per_task.png")

    plt.figure(figsize=(10, 6))
    plt.plot(task_indices, per_task_times, marker='x', color='orange', label="Time per Task (s)")
    plt.xlabel("Task Index")
    plt.ylabel("Time (seconds)")
    plt.title("Time Taken per Task")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("benchmark_results/time_per_task.png")

    # Save stats as CSV
    import pandas as pd
    stats_df = pd.DataFrame({
        "task_index": task_indices,
        "messages_processed": per_task_messages,
        "time_seconds": per_task_times,
    })
    stats_df.to_csv("benchmark_results/benchmark_stats.csv", index=False)

    assert count == NUM_TASKS
    assert throughput >= MIN_THROUGHPUT, f"Throughput too low: {throughput:.2f} tasks/sec"
