import time
from collections import Counter
from app.pipeline.base.processing_stage import ProcessingStage
from app.core.models.message import ScrapingContext
from app.core.services.feed_back_service import FeedbackService

class FeedbackStage(ProcessingStage):
    def __init__(self, feedback_service: FeedbackService, interval_minutes: int = 1, top_k: int = 5):
        self.feedback_service = feedback_service
        self.interval = interval_minutes * 60  # convert to seconds
        self.top_k = top_k
        self.last_sent_time = time.time()
        self.entity_counter = Counter()

    async def process(self, scraping_context: ScrapingContext, nextStep=None):
        for msg in scraping_context.messages:
            named_entities = msg.metadata.get("named_entities", [])
            for entity in named_entities:
                self.entity_counter[entity["text"]] += 1

        current_time = time.time()
        if current_time - self.last_sent_time >= self.interval:
            top_entities = self.entity_counter.most_common(self.top_k)
            payload = {
                "domain": scraping_context.task.domain,
                "timestamp": time.time(),
                "top_named_entities": [{"text": text, "count": count} for text, count in top_entities],
            }
            self.feedback_service.send_feedback(payload)
            self.entity_counter.clear()
            self.last_sent_time = current_time

        if nextStep:
            return await nextStep.process(scraping_context)
        return scraping_context
