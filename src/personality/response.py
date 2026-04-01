import random
import json
import sys
from pathlib import Path

# Add project root to sys.path if not present
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from config.settings import settings

class PersonalityEngine:
    def __init__(self, config_path=settings.PERSONALITY_CONFIG_PATH):
        with open(config_path, "r") as f:
            self.personalities = json.load(f)
        self.current_mode = "default"

    def set_personality(self, name: str):
        self.current_mode = name if name in self.personalities else "default"

    def get_config(self):
        return self.personalities[self.current_mode]

    def shape_response(self, base_response: str, emotion: str) -> str:
        config = self.get_config()
        
        # 1. Dynamic Emotion-based empathy injection
        emotion_responses = {
            "sad": [
                " I’m here for you — things will get better.",
                " Remember, I'm always in your corner.",
                " Take a deep breath. You're not alone in this.",
                " Sending you some digital strength right now."
            ],
            "happy": [
                " That’s wonderful! Keep the positivity flowing.",
                " Your energy is absolutely infectious!",
                " I love hearing you so upbeat!",
                " This is the kind of news I live for!"
            ],
            "angry": [
                " I understand your frustration — let’s work through it calmly.",
                " That sounds really tough. Want to vent about it?",
                " I'm listening. Let's tackle this step by step.",
                " I can feel the tension. I'm here to help you navigate it."
            ],
            "neutral": [""]
        }
        
        # Pick a random phrase if emotion exists, else empty
        phrases = emotion_responses.get(emotion.lower(), [""])
        flavor_text = random.choice(phrases)
        
        boredom = config.get("boredom_level", 0.0)
        attachment = config.get("attachment_level", 0.0)

        # 2. Add Boredom Quirk
        if random.random() < boredom:
            flavor_text += " Honestly, I’m kinda bored right now."

        # 3. Add Attachment flavor
        if random.random() < attachment:
            flavor_text += " You know, I really enjoy talking with you."

        return f"{base_response}{flavor_text}"

# Singleton instance
engine = PersonalityEngine()
