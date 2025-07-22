from typing import Optional
from app.core.models.message import ScrapingContext
from app.core.services.logging_service import LoggingService
from app.core.services.twet_embedding_service import TweetEmbeddingService
from app.pipeline.base.processing_stage import ProcessingStage

logger = LoggingService("TweetEmbeddingStage").get_logger()

class EmbeddingStage(ProcessingStage):
    def __init__(self):
        super().__init__()
        self.embedding_service = TweetEmbeddingService()

    async def process(self, scraping_context: ScrapingContext, nextStep: Optional[ProcessingStage] = None) -> ScrapingContext:
        texts = [msg.content for msg in scraping_context.messages]

        try:
            embeddings = self.embedding_service.embed_texts(texts)
            for msg, emb in zip(scraping_context.messages, embeddings):
                msg.embedding = emb
            print("[INFO] Embeddings generated successfully.")
        except Exception as e:
            logger.error(f"[Batch Error] Failed to generate embeddings: {e}")
            for msg in scraping_context.messages:
                msg.embedding = None
                msg.metadata["embedding"] = None

        if nextStep:
            return await nextStep.process(scraping_context)

        return scraping_context
