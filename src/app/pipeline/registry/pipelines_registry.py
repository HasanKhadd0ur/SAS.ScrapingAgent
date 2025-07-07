from app.core.ml_models.sentiment_analysis_model import SentimentAnalysisModel
from app.core.services.feed_back_service import FeedbackService
from app.core.services.ner_service import NERService
from app.kafka.kafka_producer import KafkaProducer
from app.pipeline.stages.feedback_stage import FeedbackStage
from app.pipeline.stages.hate_speach_processing_stage import HateSpeachProcessingStage
from app.pipeline.stages.keyword_processing_stage import KeywordProcessingStage
from app.pipeline.stages.master_notifying_stage import MasterNotifyingStage
from app.pipeline.stages.messages_publishing_stage import MessagesPublishingStage
from app.pipeline.stages.messages_saving_stage import MessagesSavingStage
from app.pipeline.stages.named_entities_extraction_stage import NamedEntitiesExtractionStage
from app.pipeline.stages.normalize_text_stage import NormalizeTextStage
from app.pipeline.stages.sentiment_analysis_stage import SentimentAnalysisStage

# Shared dependency instances (singletons or factories)
shared_dependencies = {
    "SAModel": SentimentAnalysisModel(),
    "NERService":NERService(),
    "FeedbackService": FeedbackService(KafkaProducer(), topic="scraping-feedback")

    # Add more shared dependencies here if needed
}

STAGE_CLASS_MAP = {
    "KeywordFilterStage": {
        "class": KeywordProcessingStage,
        "dependencies": []
    },
    "NormalizeTextStage": {
        "class": NormalizeTextStage,
        "dependencies": []
    },
    "MessagesPublishingStage": {
        "class": MessagesPublishingStage,
        "dependencies": []
    },
    "SentimentAnalysisStage": {
        "class": SentimentAnalysisStage,
        "dependencies": ["SAModel"]
    },
    "HateSpeachFilteringStage": {
        "class": HateSpeachProcessingStage,
        "dependencies": []
    },
    "MessagesSavingStage": {
        "class": MessagesSavingStage,
        "dependencies": []
    },
    "MasterNotifyingStage": {
        "class": MasterNotifyingStage,
        "dependencies": []
    },
    "NamedEntitiesExtractionStage": {
        "class": NamedEntitiesExtractionStage,
        "dependencies": ["NERService"]
    },
     "FeedbackStage": {
        "class": FeedbackStage,
        "dependencies": ["FeedbackService"]
    }
}