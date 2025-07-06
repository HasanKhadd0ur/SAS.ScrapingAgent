from typing import Any, List
from app.core.configs.env_config import EnvSettings
from app.core.ml_models.sentiment_analysis_model import SentimentAnalysisModel
from app.pipeline.pipeline import Pipeline
from app.pipeline.stages.hate_speach_processing_stage import HateSpeachProcessingStage
from app.pipeline.stages.keyword_processing_stage import KeywordProcessingStage
from app.pipeline.stages.master_notifying_stage import MasterNotifyingStage
from app.pipeline.stages.messages_publishing_stage import MessagesPublishingStage
from app.pipeline.stages.messages_saving_stage import MessagesSavingStage
from app.pipeline.stages.normalize_text_stage import NormalizeTextStage
from app.pipeline.stages.sentiment_analysis_stage import SentimentAnalysisStage

# Map short names to actual classes manually or via dynamic import
STAGE_CLASS_MAP = {
    "KeywordFilterStage": KeywordProcessingStage,
    "NormalizeTextStage": NormalizeTextStage,
    "MessagesPublishingStage": MessagesPublishingStage,
    "SentimentAnalysisStage": SentimentAnalysisStage,
    "HateSpeachFilteringStage": HateSpeachProcessingStage,
    "MessagesSavingStage": MessagesSavingStage,
    "MasterNotifyingStage": MasterNotifyingStage,
}

def get_stage_instance(stage_name: str, args: List[Any] = None):
    cls = STAGE_CLASS_MAP.get(stage_name)
    if not cls:
        raise ValueError(f"Unknown stage: {stage_name}")
    if args:
        return cls(*args)
    return cls()

settings = EnvSettings()
pipeline_config = settings.get_pipeline_config()

# Rebuild preprocessing pipeline
preprocessing_pipeline = Pipeline()
SAModel = SentimentAnalysisModel()  # instantiate your model once

for stage_info in pipeline_config["PREPROCESSING_PIPELINE"]:
    stage_name = stage_info["stage"]
    args = None
    # If this stage needs the model, inject it here
    if "args" in stage_info:
        args=[]
        for arg_name in stage_info["args"]:
            if arg_name == "SAModel":
                args.append(SAModel)
            else:
                # Add other dependencies if needed
                pass
    # instance = get_stage_instance(stage_name, args)
    cls = STAGE_CLASS_MAP.get(stage_name)
    if args :
        preprocessing_pipeline.add_filter(cls,*args)
    else: 
        preprocessing_pipeline.add_filter(cls)
   

# Similarly, rebuild publishing pipeline
publishing_pipeline = Pipeline()
for stage_info in pipeline_config["PUBLISHING_PIPELINE"]:
    # instance = get_stage_instance(stage_info["stage"])
    publishing_pipeline.add_filter(STAGE_CLASS_MAP.get(stage_info["stage"]))