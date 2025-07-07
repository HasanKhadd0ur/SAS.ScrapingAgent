from app.pipeline.registry.pipelines_registry import STAGE_CLASS_MAP, shared_dependencies
from app.pipeline.pipeline import Pipeline

class PipelineFactory:
    def __init__(self, pipeline_config):
        self.pipeline_config = pipeline_config

    def _get_stage_class_and_args(self, stage_name):
        stage_info = STAGE_CLASS_MAP.get(stage_name)
        if not stage_info:
            raise ValueError(f"Unknown stage: {stage_name}")
        
        cls = stage_info["class"]
        deps = stage_info.get("dependencies", [])
        args = [shared_dependencies[dep] for dep in deps]
        return cls, args

    def build_pipeline(self, pipeline_key):
        pipeline = Pipeline()
        stages_info = self.pipeline_config[pipeline_key]

        for stage in stages_info:
            stage_name = stage["stage"]
            print(stage_name)
            cls, args = self._get_stage_class_and_args(stage_name)
            pipeline.add_filter(cls, *args)

        return pipeline
