from app.core.ml.sentiment_analysis_model import SentimentAnalysisModel
from app.pipeline.base import FilterStage
from app.core.models.message import ScrapingContext

class SentimentAnalysisStage(FilterStage):
    def __init__(self, sentiment_model: SentimentAnalysisModel):
        super().__init__()
        self.sentiment_model = sentiment_model

    async def process(self, scraping_context : ScrapingContext, nextStep: FilterStage = None) -> ScrapingContext:
        for message in scraping_context.messages:
            # print(message.content)
            sentiment_score = self.sentiment_model.analyze(text=message.content)
            message.sentiment_score = sentiment_score
            message.sentiment_label = "positive" if sentiment_score > 0.5 else "negative"
        
        if nextStep:
            return await nextStep.process(scraping_context)
        return scraping_context
