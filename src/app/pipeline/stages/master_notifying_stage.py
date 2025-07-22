from app.pipeline.base.processing_stage import ProcessingStage
from app.core.models.message import  ScrapingContext

class MasterNotifyingStage(ProcessingStage):

    async def process(self, scraping_context : ScrapingContext, nextStep: ProcessingStage = None) -> ScrapingContext:
        # To Do 
        # Here we should notify the master (scraping manager) in the result of the task        
        # print(f"[+] Finished processing batch for task '{scraping_context.task.id}'")

        if nextStep:
            return await nextStep.process(scraping_context)
        return scraping_context
