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
        
        boredom = config.get("boredom_level", 0.0)
        attachment = config.get("attachment_level", 0.0)

        # 1. Emotion-based empathy injection
        emotion_responses = {
            "sad": " I’m here for you — things will get better.",
            "happy": " That’s wonderful! Keep the positivity flowing.",
            "angry": " I understand your frustration — let’s work through it calmly.",
            "neutral": ""
        }
        
        # Only add emotion text if it's not neutral
        flavor_text = emotion_responses.get(emotion, "")
        
        # 2. Add Boredom Quirk
        if random.random() < boredom:
            flavor_text += " Honestly, I’m kinda bored right now."

        # 3. Add Attachment flavor
        if random.random() < attachment:
            flavor_text += " You know, I really enjoy talking with you."

        return f"{base_response}{flavor_text}"

engine = PersonalityEngine()