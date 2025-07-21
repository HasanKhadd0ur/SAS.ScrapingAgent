import pytest
import time
from unittest.mock import patch, MagicMock

from app.agent import Agent
from app.scrapers.sources.dummy.dummy_file_scrarper import DummyFileScraper
from tests.mocks.mock_test import MockTasksService
from app.pipeline.factory.default_pipelines import preprocessing_pipeline, publishing_pipeline
from app.core.configs.env_config import EnvConfig

@pytest.mark.asyncio
async def test_throughput_with_mocked_kafka():
    NUM_TASKS = 100
    MIN_THROUGHPUT = 2.0  # tasks/sec

    # Mock Kafka producer
    # mock_producer = MagicMock()
    # mock_producer.send.return_value = None
    # mock_producer_class.return_value = mock_producer

    tasks_service = MockTasksService(NUM_TASKS)
    dummy_scraper = DummyFileScraper(config_service=EnvConfig())

    agent = Agent(
        scraper=dummy_scraper,
        preprocessing_pipeline=preprocessing_pipeline,
        publishing_pipeline=publishing_pipeline
    )

    count = 0
    start = time.time()

    async for task in tasks_service.stream_tasks():
        agent.set_scraper(dummy_scraper)
        agent.assign_task(task)
        await agent.run()
        await tasks_service.complete_task(task.id)
        count += 1

    elapsed = time.time() - start
    throughput = count / elapsed

    print(f"\nProcessed {count} tasks in {elapsed:.2f}s. Throughput = {throughput:.2f} tasks/sec")

    assert count == NUM_TASKS
    assert throughput >= MIN_THROUGHPUT, f"Throughput too low: {throughput:.2f} tasks/sec"
