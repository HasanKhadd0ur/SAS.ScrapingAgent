from typing import AsyncGenerator

import logging

import httpx
from app.core.models.scraper_task import DataSource, ScrapingApproach, ScrapingTask
from app.kafka.kafka_consumer import KafkaConsumer

logger = logging.getLogger(__name__)

class TasksService:
    
   def __init__(self,
            kafka_topic="scraping-tasks",
            kafka_bootstrap="localhost:9092", 
            kafka_group="scraper-agent", 
            master_api_url="http://localhost:5000",
            scraper_instance_id="scraper-1"):
       
        self.consumer = KafkaConsumer(
            topic=kafka_topic,
            bootstrap_servers=kafka_bootstrap,
            group_id=kafka_group,
            group_instance_id=scraper_instance_id
        )
        self.master_api_url = master_api_url 
    

   async def complete_task(self, task_id: str) -> bool:
        url = f"{self.master_api_url}/api/scrapingtasks/{task_id}/complete"
        async with httpx.AsyncClient(verify=False) as client:
            try:
                response = await client.post(url)
                response.raise_for_status()
                logger.info(f"Task {task_id} marked complete successfully.")
                print(f"[INFO] Task {task_id} marked complete successfully.")
                return True
            except httpx.HTTPStatusError as e:
                logger.error(f"Failed to complete task {task_id}: {e.response.status_code} - {e.response.text}")
                print(f"[ERROR] Failed to complete task {task_id}: {e.response.status_code} - {e.response.text}")
            except Exception as e:
                logger.error(f"Unexpected error completing task {task_id}: {e}")
                print(f"[ERROR] Unexpected error completing task {task_id}: {e}")
        return False
    
   async def assign_executor(self, scraping_task_id: str, scraper_id: str) -> bool:
        url = f"{self.master_api_url}/api/scrapingtasks/assign"
        payload = {
            "scrapingTaskId": scraping_task_id,
            "scraperId": scraper_id
        }
        async with httpx.AsyncClient(verify=False) as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                logger.info(f"Assigned scraper {scraper_id} to task {scraping_task_id} successfully.")
                print(f"[INFO] Assigned scraper {scraper_id} to task {scraping_task_id} successfully.")
                return True
            except httpx.HTTPStatusError as e:
                logger.error(f"Failed to assign scraper {scraper_id} to task {scraping_task_id}: {e.response.status_code} - {e.response.text}")
                print(f"[ERROR] Failed to assign scraper {scraper_id} to task {scraping_task_id}: {e.response.status_code} - {e.response.text}")
            except Exception as e:
                logger.error(f"Unexpected error assigning scraper {scraper_id} to task {scraping_task_id}: {e}")
                print(f"[ERROR] Unexpected error assigning scraper {scraper_id} to task {scraping_task_id}: {e}")
        return False
    
   async def stream_tasks(self) -> AsyncGenerator[ScrapingTask, None]:
        await self.consumer.start()
        try:
            async for msg in self.consumer.get_messages():
                try:
                    task = self._parse_task(msg)
                    yield task
                except Exception as e:
                    print(f"[Error] Failed to parse task from message: {e}")
        finally:
            await self.consumer.stop()

   def _parse_task(self, data: dict) -> ScrapingTask:
        return ScrapingTask(
            id=data["Id"],
            domain=data["Domain"],
            platform=data["Platform"],
            sources=[
                DataSource(target=ds["Target"], limit=ds.get("Limit", 1))
                for ds in data["DataSources"]
            ],
            limit=data.get("Limit", 5),
            scraping_approach=ScrapingApproach(
                name=data["ScrapingApproach"]["Name"],
                platform=data["ScrapingApproach"]["Platform"],
                mode=data["ScrapingApproach"]["Mode"]
            )
        )

    # async def stream_tasks(self) -> AsyncGenerator[ScrapingTask, None]:
    #     # Simulate streaming 3 fake tasks with small delays
    #     for i in range(300):
    #         await asyncio.sleep(0.1)  # Simulate delay between tasks
    #         yield ScrapingTask(
    #                 id=str(uuid.uuid4()), 
    #                 platform="telegram",
    #                 domain="Politics",
    #                 sources=[DataSource(target="freesyria102", limit=30)],
    #                 limit=100,
    #                 scraping_approach=ScrapingApproach(name="DummyFileScraper",platform="File",mode="Dummy")
    #             )
    #         # yield ScrapingTask(
    #         #         id=str(uuid.uuid4()), 
    #         #         platform="telegram",
    #         #         domain="Politics",
    #         #         sources=[
    #         #             # DataSource(target="freesyria102", limit=160),
    #         #             # DataSource(target="Almohrar", limit=1060),
    #         #             DataSource(target="Almohrar", limit=5)
    #         #                  ],
    #         #         limit=10,
    #         #         scraping_approach=ScrapingApproach(name="TelegramWebScraper",platform="telegram",mode="Web")
    #         #     )
    #         #  yield ScrapingTask(
    #         #         id=str(uuid.uuid4()), 
    #         #         platform="telegram",
    #         #         domain="Politics",
    #         #         sources=[
    #         #             # DataSource(target="freesyria102", limit=160),
    #         #             # DataSource(target="Almohrar", limit=1060),
    #         #             DataSource(target="MQ_QU", limit=160)
    #         #                  ],
    #         #         limit=100,
    #         #         scraping_approach=ScrapingApproach(name="TelegramTelethonScraper",platform="telegram",mode="bot")
    #         #     )
# Almohrar
# freesyria102
# MQ_QU