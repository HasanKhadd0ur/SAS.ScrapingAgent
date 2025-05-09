from app.core.ml.sentiment_analysis_model import SentimentAnalysisModel
from app.pipeline.pipeline import Pipeline
from app.pipeline.stages.messages_publishing_stage import MessagesPublishingStage
from app.pipeline.stages.keyword_filter_stage import KeywordFilterStage
from app.pipeline.stages.normalize_text_stage import NormalizeTextStage
from app.pipeline.stages.sentiment_analysis_stage import SentimentAnalysisStage

# The filter registry stores the filter instances
PIPELINE_REGISTRY = {
    "keyword_filter_stage": KeywordFilterStage,
    "normalize_stage": NormalizeTextStage,
    "messages_publishing_stage": MessagesPublishingStage
}

# The order in which filters are applied
PIPELINE_ORDER = [
    "keyword_filter_stage",
    "normalize_stage",
]

# Define a preprocessing pipelie
preprocessing_pipeline= Pipeline()
preprocessing_pipeline.add_filter(NormalizeTextStage)
SAModel =SentimentAnalysisModel()
preprocessing_pipeline.add_filter(SentimentAnalysisStage,SAModel)

# Define a publishing pipeline
publishing_pipeline= Pipeline()
publishing_pipeline.add_filter(MessagesPublishingStage)
