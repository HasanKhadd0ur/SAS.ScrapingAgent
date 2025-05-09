from typing import List
from app.core.ml.sentiment_analysis_model import SentimentAnalysisModel
from app.pipeline.base import FilterStage
from app.core.models.message import Message

class SentimentAnalysisStage(FilterStage):
    def __init__(self, sentiment_model: SentimentAnalysisModel):
        super().__init__()
        self.sentiment_model = sentiment_model

    def process(self, messages: List[Message], nextStep: FilterStage = None) -> List[Message]:
        for message in messages:
            print(message.content)
            sentiment_score = self.sentiment_model.analyze(text=message.content)
            message.sentiment_score = sentiment_score
            message.sentiment_label = "positive" if sentiment_score > 0.5 else "negative"
        
        if nextStep:
            return nextStep.process(messages)
        return messages
