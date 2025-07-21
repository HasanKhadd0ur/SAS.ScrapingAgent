from transformers import pipeline
import random

class SentimentAnalysisModel:
    def __init__(self):
        self.pipeline = pipeline(
            "sentiment-analysis", 
            model="CAMeL-Lab/bert-base-arabic-camelbert-mix-sentiment"
        )


    def analyze_batch(self, texts: list[str]) -> list[float]:
        # Simulate sentiment scores randomly
        scores = [round(random.uniform(0, 1), 3) for _ in texts]
        return scores
    # def analyze(self, text: str) -> float:
    #         result = self.pipeline(text[:512])[0]  # truncate long texts
    #         label = result['label']
    #         score = result['score']

    #         # Convert to float between 0 (negative) and 1 (positive)
    #         if label == 'Positive':
    #             return score
    #         elif label == 'Negative':
    #             return 1 - score
    #         else:  # Neutral case
    #             return 0.5
    # def analyze_batch(self, texts: list[str]) -> list[float]:
    #     results = self.pipeline([text[:512] for text in texts])  # batch input
    #     scores = []
    #     for res in results:
    #         label = res['label']
    #         score = res['score']
    #         if label == 'Positive':
    #             scores.append(score)
    #         elif label == 'Negative':
    #             scores.append(1 - score)
    #         else:
    #             scores.append(0.5)
    #     return scores
