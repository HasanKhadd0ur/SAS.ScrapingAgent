from app.pipeline.base import FilterStage
from app.core.models.message import ScrapingContext

class HateSpeachFilteringStage(FilterStage):
       
    async def process(self, scraping_context : ScrapingContext, nextStep: FilterStage = None) -> ScrapingContext:
        # To Do 
        # add hate speach model and filteing the messages

        if nextStep:
            return await nextStep.process(scraping_context)
        return scraping_context
