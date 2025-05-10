from typing import List
from app.core.models.message import Message
from app.pipeline.base import FilterStage

class Pipeline:
    def __init__(self):
        self.filters = []

    def add_filter(self, filter_stage_class :FilterStage,*args):
        """Add a filter class (that extends FilterStage) to the pipeline."""
        # Instantiate the filter class and add it to the pipeline
        self.filters.append(filter_stage_class(*args))
        return self  # Allow method chaining


    def process(self, messages: List[Message]):
        """Process the message through all the filters in the pipeline."""
        for stage in self.filters:
            messages = stage.process(messages)
        return messages