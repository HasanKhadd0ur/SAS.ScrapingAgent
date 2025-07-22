import joblib
import os

class TweetFilterModel:
    def __init__(self, model_path: str = "assets/models/grid_search_svm_model.joblib"):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at: {model_path}")
        self.model = joblib.load(model_path)

    def predict(self, embeddings: list[list[float]]) -> list[int]:
        return self.model.predict(embeddings)