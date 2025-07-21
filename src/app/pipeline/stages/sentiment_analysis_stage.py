from app.core.ml_models.sentiment_analysis_model import SentimentAnalysisModel
from app.pipeline.base.processing_stage import ProcessingStage
from app.core.models.message import ScrapingContext
from typing import  Optional

class SentimentAnalysisStage(ProcessingStage):
    def __init__(self, sentiment_model: SentimentAnalysisModel):
        super().__init__()
        self.sentiment_model = sentiment_model


    async def process(self, scraping_context: ScrapingContext, nextStep: Optional[ProcessingStage] = None) -> ScrapingContext:
        contents = [m.content for m in scraping_context.messages]
        scores = self.sentiment_model.analyze_batch(contents)
        
        for message, score in zip(scraping_context.messages, scores):
            message.sentiment_score = score
            message.sentiment_label = "positive" if score > 0.5 else "negative"

        if nextStep:
            return await nextStep.process(scraping_context)
        return scraping_context

    # async def process(self, scraping_context : ScrapingContext, nextStep: Optional[ProcessingStage] = None) -> ScrapingContext:
    #     for message in scraping_context.messages:
    #         # print(message.content)
    #         sentiment_score = self.sentiment_model.analyze(text=message.content)
    #         message.sentiment_score = sentiment_score
    #         message.sentiment_label = "positive" if sentiment_score > 0.5 else "negative"
        
    #     if nextStep:
    #         return await nextStep.process(scraping_context)
    #     return scraping_context
