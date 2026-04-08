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
        with open(config_path, "r", encoding="utf-8") as f:
            self.personalities = json.load(f)
        self.current_mode = "default"

    def set_personality(self, name: str):
        self.current_mode = name if name in self.personalities else "default"

    def get_config(self):
        return self.personalities[self.current_mode]

    def shape_response(self, base_response: str, emotion: str) -> str:
        # We rely more on the model now, but can still add occasional "quirks"
        config = self.get_config()
        
        boredom = config.get("boredom_level", 0.0)
        attachment = config.get("attachment_level", 0.0)

        flavor_text = ""
        # 1. Add Boredom Quirk (Very rarely)
        if random.random() < boredom * 0.5: # Half the chance to avoid annoyance
            quirks = [
                " (Sigh, anyway...)",
                " ...and I'm actually a bit distracted today.",
                " Sorry, my mind drifted for a second."
            ]
            flavor_text += random.choice(quirks)

        # 2. Add Attachment flavor (Very rarely)
        if random.random() < attachment * 0.5:
            quirks = [
                " You know, I'm glad you're here.",
                " Talking to you is the best part of my day.",
                " Just wanted to say you're doing great."
            ]
            flavor_text += random.choice(quirks)

        if flavor_text:
            return f"{base_response}\n\n{flavor_text.strip()}"
        return base_response

# Singleton instance
engine = PersonalityEngine()
