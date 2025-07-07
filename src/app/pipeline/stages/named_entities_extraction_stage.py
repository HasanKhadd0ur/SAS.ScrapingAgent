from app.pipeline.base.processing_stage import ProcessingStage
from app.core.models.message import ScrapingContext
from app.core.services.ner_service import NERService

class NamedEntitiesExtractionStage(ProcessingStage):
    def __init__(self, ner_service: NERService):
        self.ner_service = ner_service

    async def process(self, scraping_context: ScrapingContext, nextStep=None):
        for msg in scraping_context.messages:
            entities = self.ner_service.extract_named_entities(msg.content)
            msg.metadata["named_entities"] = [ne.__dict__ for ne in entities]

            # print("Named Entities:", msg.metadata["named_entities"])
        if nextStep:
            return await nextStep.process(scraping_context)
        return scraping_context
