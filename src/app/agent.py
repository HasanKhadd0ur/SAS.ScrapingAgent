from app.core.models.message import ScrapingContext
from app.core.models.scraper_task import ScrapingTask
from app.core.base.base import BaseScraper
from app.pipeline.pipeline import Pipeline
from app.pipeline.registry import publishing_pipeline as pub, preprocessing_pipeline as pre


class Agent:
    def __init__(
        self,
        scraper: BaseScraper,
        preprocessing_pipeline: Pipeline = pre,
        publishing_pipeline: Pipeline =pub
    ):
        self.scraper = scraper
        self.preprocessing_pipeline = preprocessing_pipeline
        self.publishing_pipeline = publishing_pipeline
        self.task: ScrapingTask = None

    def set_preprocessing_pipeline(self, pipeline: Pipeline):
        self.preprocessing_pipeline = pipeline

    def set_publishing_pipeline(self, pipeline: Pipeline):
        self.publishing_pipeline = pipeline

    def set_scraper(self, scraper: BaseScraper):
        self.scraper = scraper

    def assign_task(self, task: ScrapingTask):
        self.task = task

    async def run(self):
        if not self.task:
            raise ValueError("No task assigned to agent.")

        async for message_batch in self.scraper.run_task(self.task):
            
            context=ScrapingContext(messages=message_batch,task=self.task)       
            
            context = await self.preprocessing_pipeline.process(context)
            await self.publishing_pipeline.process(context)
