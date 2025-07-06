from transformers import pipeline

class SentimentAnalysisModel:
    def __init__(self):
        self.pipeline = pipeline("sentiment-analysis")

    def analyze(self, text: str) -> float:
        result = self.pipeline(text[:512])[0]  # truncate long texts
        score = result['score']
        return score if result['label'] == 'POSITIVE' else 1 - score
