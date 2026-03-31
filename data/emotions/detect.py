from transformers import pipeline

# Load emotion classifier (DistilRoBERTa fine-tuned on GoEmotions)
emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True
)

def detect_emotion(user_input: str) -> str:
    results = emotion_classifier(user_input)
    emotion = max(results[0], key=lambda x: x['score'])['label']
    return emotion