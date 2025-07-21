from transformers import pipeline

class SentimentAnalysisModel:
    def __init__(self):
        self.pipeline = pipeline(
            "sentiment-analysis", 
            model="CAMeL-Lab/bert-base-arabic-camelbert-mix-sentiment"
        )

    def analyze(self, text: str) -> float:
            result = self.pipeline(text[:512])[0]  # truncate long texts
            label = result['label']
            score = result['score']

            # Convert to float between 0 (negative) and 1 (positive)
            if label == 'Positive':
                return score
            elif label == 'Negative':
                return 1 - score
            else:  # Neutral case
                return 0.5