import requests
import json
import sys
from pathlib import Path

# Add project root to sys.path if not present
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.utils.logger import logger
from config.settings import settings

def generate_proactive_suggestion(user_facts, personality_config):
    """
    Analyzes user skills and suggests the next logical step in their learning journey
    using Ollama.
    """
    model_id = settings.GPT_MODEL_ID
    ollama_url = f"{settings.OLLAMA_HOST}/api/chat"
    
    skills = [f['value'] for f in user_facts if f['category'] == 'skill']
    goals = [f['value'] for f in user_facts if f['category'] == 'goal']
    
    if not skills:
        return None

    skills_str = ", ".join(skills)
    goals_str = ", ".join(goals) if goals else "general professional growth"

    system_msg = (
        "You are Aura's strategic thinking core. Your job is to look at a user's current tech stack "
        "and suggest a 'Next Big Step'. "
        "Be specific, technical, and encouraging. Suggest a complex, 'product-ready' project idea or a "
        "specific advanced technology that complements their existing skills. "
        f"The user knows: {skills_str}. Their goals are: {goals_str}. "
        "Talk directly to the user as Aura. Do not use any prefixes or headers like '[Autonomous Reflection]'. "
        "Keep it concise but high-impact (2-3 sentences)."
    )

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": "What should I focus on next?"}
    ]

    payload = {
        "model": model_id,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.8,
            "num_predict": 150
        }
    }

    try:
        response = requests.post(ollama_url, json=payload, timeout=15)
        response.raise_for_status()
        result = response.json()
        return result['message']['content'].strip()
    except Exception as e:
        logger.error(f"❌ Proactive Reflection Error: {e}")
        return None
