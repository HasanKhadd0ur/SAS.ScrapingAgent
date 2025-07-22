from typing import Optional
from app.core.ml_models.tweet_filter_model import TweetFilterModel
from app.core.models.message import ScrapingContext
from app.core.services.logging_service import LoggingService
from app.pipeline.base.processing_stage import ProcessingStage

logger = LoggingService("TweetFilterStage").get_logger()

class MessagesClasificationStage(ProcessingStage):
    def __init__(self, model_path: str = "assets/models/grid_search_svm_model.joblib"):
        super().__init__()
        self.model = TweetFilterModel(model_path)
 
    async def process(self, scraping_context: ScrapingContext, nextStep: Optional[ProcessingStage] = None) -> ScrapingContext:
        messages = scraping_context.messages
        embeddings = [msg.embedding for msg in messages]

        print(f"[INFO] Starting classification with {len(messages)} messages")

        if not embeddings:
            logger.warning("[ERROR] No embeddings found.")
            print("[ERROR] No embeddings found in messages.")
            return scraping_context

        try:
            predictions = self.model.predict(embeddings)

            filtered_messages = [msg for msg, pred in zip(messages, predictions) if pred == 1]
            print(f"[INFO] Filtered out {len(messages) - len(filtered_messages)} messages.")

            # logger.info(f"[INFO] Filtered {len(messages) - len(filtered_messages)} messages out of {len(messages)}.")
            scraping_context.messages = filtered_messages

        except Exception as e:
            logger.error(f"[ERROR] Error filtering tweets: {e}")
            print(f"[ERROR] Exception during prediction: {e}")

        if nextStep:
            return await nextStep.process(scraping_context)

        return scraping_context
