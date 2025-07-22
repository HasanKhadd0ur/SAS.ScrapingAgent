from app.pipeline.base.processing_stage import ProcessingStage
from app.core.models.message import ScrapingContext
from app.core.services.ner_service import NERService

class NamedEntitiesExtractionStage(ProcessingStage):
    def __init__(self, ner_service: NERService):
        self.ner_service = ner_service

    async def process(self, scraping_context: ScrapingContext, nextStep=None):
        contents = [msg.content for msg in scraping_context.messages]
        all_entities = self.ner_service.extract_named_entities_batch(contents)
        
        for msg, ents in zip(scraping_context.messages, all_entities):
            msg.metadata["named_entities"] = [ne.__dict__ for ne in ents]
            
        print(f"[INFO] Extracted named entities for the task :{len(scraping_context.task.id)} messages.")

        if nextStep:
            return await nextStep.process(scraping_context)
        return scraping_context
