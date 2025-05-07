from app.core.models.message import Message

class FilterStage:
    def process(self, message: Message, nextStep: 'FilterStage' = None):
        """
        This method should be implemented by each filter to process the message.
        If a next filter exists, the message should be passed to it.
        """
        raise NotImplementedError("Filter must implement `process()`")
