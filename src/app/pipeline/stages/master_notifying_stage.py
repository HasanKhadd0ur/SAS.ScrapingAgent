from app.pipeline.base import FilterStage
from app.core.models.message import  ScrapingContext

class MasterNotifyingStage(FilterStage):

    async def process(self, scraping_context : ScrapingContext, nextStep: FilterStage = None) -> ScrapingContext:
        # To Do 
        # Here we should notify the master (scraping manager) in the result of the task        
        print(f"[+] Finished processing batch for task '{scraping_context.task.id}'")

        if nextStep:
            return await nextStep.process(scraping_context)
        return scraping_context
