from sentence_transformers import SentenceTransformer
import torch
from app.core.services.logging_service import LoggingService

logger = LoggingService("TweetEmbeddingStage").get_logger()

class TweetEmbeddingService:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", device=self.device)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            logger.warning("[Warning] Empty list received for batch embedding.")
            return []

        try:
            embeddings = self.model.encode(texts, convert_to_tensor=False, show_progress_bar=False)
            return embeddings  
        except Exception as e:
            logger.error(f"[ERROR] Failed batch embedding: {e}")
            return [None] * len(texts)
