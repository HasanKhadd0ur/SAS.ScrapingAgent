from app.core.models.message import ScrapingContext

class FilterStage:
    async def process(self, scraping_context : ScrapingContext, nextStep: 'FilterStage' = None) -> ScrapingContext:
        """
        This method should be implemented by each filter to process the message.
        If a next filter exists, the message should be passed to it.
        """
        raise NotImplementedError("Filter must implement `process()`")
