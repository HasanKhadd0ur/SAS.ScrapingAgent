from app.core.models.message import Message

class FilterStage:
    async def process(self, messages: list[Message], nextStep: 'FilterStage' = None) -> list[Message]:
        """
        This method should be implemented by each filter to process the message.
        If a next filter exists, the message should be passed to it.
        """
        raise NotImplementedError("Filter must implement `process()`")
