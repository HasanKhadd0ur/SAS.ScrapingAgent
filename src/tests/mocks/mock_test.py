from app.core.models.scraper_task import ScrapingApproach


class MockTask:
    def __init__(self, id, scraping_approach= ScrapingApproach()):
        self.id = id
        self.scraping_approach :ScrapingApproach = scraping_approach
        self.domain='Politics'
        self.platform='Telegram'


class MockTasksService:
    def __init__(self, num_tasks):
        self.num_tasks = num_tasks

    async def stream_tasks(self):
        for i in range(self.num_tasks):
            yield MockTask(id=f"task-{i}")

    async def assign_executor(self, scraper_id, scraping_task_id):
        pass

    async def complete_task(self, task_id):
        pass

