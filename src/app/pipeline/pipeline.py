from app.core.models.message import Message

class Pipeline:
    def __init__(self):
        self.filters = []

    def add_filter(self, filter_stage_class):
        """Add a filter class (that extends FilterStage) to the pipeline."""
        # Instantiate the filter class and add it to the pipeline
        self.filters.append(filter_stage_class())
        return self  # Allow method chaining


    def process(self, message: Message):
        """Process the message through all the filters in the pipeline."""
        for stage in self.filters:
            message = stage.process(message)
        return message