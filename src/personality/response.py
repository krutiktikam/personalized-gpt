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
        config = self.personalities[self.current_mode]
        print(f"DEBUG: Current Mode: {self.current_mode}")
        print(f"DEBUG: Selected Config Prefix: '{config.get('prefix')}'")
        return config

    def shape_response(self, base_response: str, emotion: str) -> str:
        """
        Final safety pass and persona hardening. 
        Removes any robotic headers or AI-assistant hallucinations.
        """
        # 1. Remove robotic headers
        cleaned = base_response.replace("[Autonomous Reflection]", "").strip()
        
        # 2. Hard-filter generic AI phrases (The "Kill-Switch")
        hallucination_patterns = [
            "I am Aura, your AI assistant",
            "I am your AI assistant",
            "How can I help you today?",
            "How can I assist you today?",
            "How can I help you?",
            "How can I assist you?",
            "As an AI model",
            "As an AI language model",
            "I don't have feelings",
            "I am programmed to",
            "I don't have a physical body",
            "Let me know if you have more questions",
            "I hope this helps",
            "Is there anything else I can help with?",
            "Happy to help",
            "Feel free to ask",
            "Let me know if you need anything else",
            "I'm here to help"
        ]
        
        for pattern in hallucination_patterns:
            if cleaned.lower().startswith(pattern.lower()):
                cleaned = cleaned[len(pattern):].lstrip(' ,.!')
            elif pattern.lower() in cleaned.lower():
                # If it's in the middle, we just remove it
                import re
                cleaned = re.sub(re.escape(pattern), "", cleaned, flags=re.IGNORECASE).strip()

        # 3. Clean up generic endings
        generic_endings = ["how can i help you?", "how can i help?", "is there anything else?", "anything else I can help with?"]
        for ending in generic_endings:
            if cleaned.lower().endswith(ending):
                cleaned = cleaned[:-len(ending)].strip().rstrip(',.!')
                if not cleaned.endswith('.'):
                    cleaned += "..."

        return cleaned.strip()

# Singleton instance
engine = PersonalityEngine()
