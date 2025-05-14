from app.core.models.message import ScrapingContext
from app.pipeline.base import FilterStage

class Pipeline:
    def __init__(self):
        self.filters = []

    def add_filter(self, filter_stage_class :FilterStage,*args):
        """Add a filter class (that extends FilterStage) to the pipeline."""
        # Instantiate the filter class and add it to the pipeline
        self.filters.append(filter_stage_class(*args))
        return self  # Allow method chaining


    async def process(self, scraping_context : ScrapingContext):
        """Process the message through all the filters in the pipeline."""
        for stage in self.filters:
            scraping_context = await stage.process(scraping_context)
        return scraping_context