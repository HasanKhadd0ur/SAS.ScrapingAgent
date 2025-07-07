from app.pipeline.base.processing_stage import ProcessingStage
from app.core.models.message import ScrapingContext

class HateSpeachProcessingStage(ProcessingStage):
       
    async def process(self, scraping_context : ScrapingContext, nextStep: ProcessingStage = None) -> ScrapingContext:
        # To Do 
        # add hate speach model and filteing the messages

        if nextStep:
            return await nextStep.process(scraping_context)
        return scraping_context
