from transformers import pipeline
import sys
from pathlib import Path

# Add project root to sys.path if not present
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from config.settings import settings

# Load a lightweight, fast emotion classifier
# This model recognizes: joy, sadness, anger, fear, surprise, love
classifier = pipeline(
    "text-classification", 
    model=settings.EMOTION_MODEL_ID, 
    top_k=1
)

from src.utils.logger import logger

def detect_emotion(text: str) -> str:
    """
    Analyzes text and returns the dominant emotion label.
    """
    try:
        results = classifier(text)
        # result looks like: [[{'label': 'joy', 'score': 0.98}]]
        emotion = results[0][0]['label']

        # Map model labels to your existing shape_response categories
        mapping = {
            "joy": "happy",
            "love": "happy",
            "sadness": "sad",
            "anger": "angry",
            "fear": "sad",
            "surprise": "happy"
        }
        return mapping.get(emotion, "neutral")
    except Exception as e:
        logger.error(f"Emotion Detection Error: {e}")
        return "neutral"