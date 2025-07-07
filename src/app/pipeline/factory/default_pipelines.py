
from app.core.configs.env_config import EnvSettings
from app.pipeline.factory.pipeline_factory import PipelineFactory


settings = EnvSettings()

pipeline_config = settings.get_pipeline_config()

factory = PipelineFactory(pipeline_config)

preprocessing_pipeline = factory.build_pipeline("PREPROCESSING_PIPELINE")
publishing_pipeline = factory.build_pipeline("PUBLISHING_PIPELINE")
