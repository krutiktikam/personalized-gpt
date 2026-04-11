import requests
import json
from src.utils.memory import memory
from src.utils.logger import logger
from config.settings import settings

def plan_work_sprint(availability, focus_area="Portfolio"):
    """
    Generates a step-by-step schedule for the user based on their free time using Ollama.
    """
    model_id = settings.GPT_MODEL_ID
    ollama_url = f"{settings.OLLAMA_HOST}/api/chat"
    
    # Get user skills and current tasks to make the plan relevant
    prefs = memory.get_preferences()
    skills = [p['value'] for p in prefs if p['category'] == 'skill']
    tasks = memory.get_tasks(status='pending')
    
    system_msg = (
        "You are Aura's Strategic Planning Module. "
        "The user has given you their availability. Create a detailed, day-wise or hour-wise "
        "work schedule for their portfolio project. "
        f"User Skills: {', '.join(skills) if skills else 'Not specified yet'}. "
        f"Pending Tasks: {', '.join([t['name'] for t in tasks]) if tasks else 'None yet'}. "
        "Talk directly to the user as Aura. Keep the tone encouraging, technical, and high-impact. "
        "Suggest specific project ideas if they have no tasks. Use Markdown formatting."
    )

    prompt = f"I am free at these times: {availability}. Create a schedule for me."

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": prompt}
    ]

    payload = {
        "model": model_id,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 500
        }
    }

    try:
        response = requests.post(ollama_url, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result['message']['content'].strip()
    except Exception as e:
        logger.error(f"❌ Scheduling Error: {e}")
        return "I'm sorry, I couldn't generate a schedule right now. Let's try again in a bit."

if __name__ == "__main__":
    # Test
    print(plan_work_sprint("Tomorrow from 6 PM to 9 PM"))