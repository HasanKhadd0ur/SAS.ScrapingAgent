from app.pipeline.pipeline import Pipeline
from app.pipeline.stages.keyword_filter import KeywordFilter

# The filter registry stores the filter instances
PIPELINE_REGISTRY = {
    "keyword_filter": KeywordFilter,
}

# The order in which filters are applied
PIPELINE_ORDER = [
    "keyword_filter"
]

default_pipeline= Pipeline()
default_pipeline.add_filter(KeywordFilter)
