import requests
import json
import re
from src.utils.logger import logger
from config.settings import settings

def extract_facts(user_input):
    """
    Extracts personal facts from user input using Ollama.
    Returns a list of dicts: [{"category": "...", "value": "..."}]
    """
    model_id = settings.GPT_MODEL_ID
    ollama_url = f"{settings.OLLAMA_HOST}/api/chat"

    system_msg = (
        "Extract personal facts from the user's message. Focus on: "
        "- 'name': The user's name (e.g., 'My name is Krutik') "
        "- 'skill': technologies or tools they know (e.g. React, Python) "
        "- 'availability': when they are free to work (e.g. tomorrow 6pm, weekend) "
        "- 'goal': what they want to achieve (e.g. build a portfolio, learn CSS) "
        "- 'preference': general likes/dislikes. "
        "Output ONLY a JSON list of objects with 'category' and 'value'. "
        "Example: [{\"category\": \"name\", \"value\": \"Krutik\"}]. "
        "If no relevant facts are found, output []."
    )

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_input}
    ]

    payload = {
        "model": model_id,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.0,  # Zero temperature for deterministic JSON output
            "num_predict": 100
        }
    }

    try:
        response = requests.post(ollama_url, json=payload, timeout=45)
        response.raise_for_status()
        result = response.json()
        response_text = result['message']['content'].strip()
        
        # DEBUG: Log the raw extraction output
        logger.info(f"🔍 RAW EXTRACTION: {response_text}")

        # Try to find JSON in the response
        match = re.search(r'\[.*?\]', response_text, re.DOTALL)
        if match:
            facts = json.loads(match.group(0))
            if isinstance(facts, list):
                return facts
        return []
    except Exception as e:
        logger.error(f"❌ Fact Extraction Error: {e}")
        return []
