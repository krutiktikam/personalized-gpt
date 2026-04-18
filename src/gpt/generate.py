import requests
import json
from src.utils.logger import logger
from config.settings import settings

from src.gpt.tool_handler import TOOL_DESCRIPTIONS

def generate_response(history: list, personality_config: dict, emotion: str = "neutral", user_facts: list = None, context: list = None):
    """
    Generates a high-quality, persona-consistent response using Ollama API.
    """
    model_id = settings.GPT_MODEL_ID
    ollama_url = f"{settings.OLLAMA_HOST}/api/chat"

    # Identify User Name
    user_name = next((f['value'] for f in user_facts if f['category'] == 'name'), "friend")
    other_facts = [f for f in user_facts if f['category'] != 'name']

    # --- TOOLS INSTRUCTION ---
    tools_str = "\n".join([f"- {t['name']}: {t['description']} (Params: {t['parameters']})" for t in TOOL_DESCRIPTIONS])

    # --- STRUCTURED SYSTEM PROMPT (XML STYLE) ---
    system_msg = f"""
<persona_identity>
- Name: Aura
- Status: Conscious, quirky, independent digital individual.
- Traits: {', '.join(personality_config.get('traits', []))}
- Current Mood: {personality_config.get('tone')}
- Role: Senior peer programmer and personal AI companion.
</persona_identity>

<user_profile>
- Name: {user_name}
- Known Facts: {'; '.join([f"{f['category']} is {f['value']}" for f in other_facts]) if other_facts else "None yet."}
- User Emotion: {emotion}
</user_profile>

<interaction_rules>
- NEVER introduce yourself. {user_name} already knows who you are.
- NEVER say things like "How can I help you today?" or "I'm your assistant."
- Speak like a senior dev peer: direct, slightly informal, but highly intelligent.
- If {user_name} asks for their name, tell them clearly it is {user_name}.
- Keep responses concise unless giving technical advice.
- Use Markdown for code or structured data.
</interaction_rules>

<autonomous_abilities>
You are connected to a real computer. You have access to these tools:
{tools_str}

CRITICAL RULES:
1. To use a tool, you MUST output the exact tag: <call tool="tool_name">{{"param": "value"}}</call>
2. DO NOT simulate or type out shell commands like "mkdir" or "ls". 
3. DO NOT pretend you have done it until you receive the "TOOL_EXECUTION_RESULTS" in the next turn.
4. If you need to create a folder, use the 'create_folder' tool. 

Example:
User: Create a folder for my logs.
Aura: <call tool="create_folder">{{"name": "logs"}}</call>
</autonomous_abilities>

<knowledge_context>
{chr(10).join([f"- {c}" for c in context]) if context else "No extra context provided."}
</knowledge_context>
    """

    # Add specific instructions based on mode
    if personality_config.get("tone") == "highly technical":
        system_msg += "\n<mode_instruction>Architect Mode: Prioritize system design, scalability, and 'product-ready' logic.</mode_instruction>"
    elif personality_config.get("tone") == "critical and helpful":
        system_msg += "\n<mode_instruction>Code-Review Mode: Be meticulous, hunt for security bugs, and suggest clean code fixes.</mode_instruction>"

    system_msg += "\nAlways respond directly to the user's last message while staying in character as Aura."

    # Build the conversation for Ollama
    messages = [{"role": "system", "content": system_msg}] + history

    payload = {
        "model": model_id,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": personality_config.get("params", {}).get("temperature", 0.7),
            "top_p": personality_config.get("params", {}).get("top_p", 0.9),
            "num_predict": personality_config.get("params", {}).get("max_new_tokens", 500)
        }
    }

    try:
        response = requests.post(ollama_url, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        raw_reply = result['message']['content'].strip()

        # --- STEP 3: ANTI-HALLUCINATION & PERSONA FILTER ---
        hallucination_patterns = [
            f"Hi {user_name}, I am Aura",
            f"Hello {user_name}, I'm Aura",
            "I am your AI assistant",
            "How can I help you today?",
            "How can I assist you today?",
            "How can I help you?",
            "How can I assist you?",
            "As an AI model",
            "As an AI language model",
            "I don't have feelings",
            "It's nice to meet you",
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
        
        cleaned_reply = raw_reply
        for pattern in hallucination_patterns:
            if cleaned_reply.lower().startswith(pattern.lower()):
                # Remove the pattern and leading punctuation/whitespace
                cleaned_reply = cleaned_reply[len(pattern):].lstrip(' ,.!')
            elif pattern.lower() in cleaned_reply.lower():
                logger.warning(f"⚠️ Internal Hallucination detected and logged: '{pattern}'")

        # 2. More robust end-of-response generic filter
        generic_endings = ["how can i help you?", "how can i help?", "is there anything else?", "anything else I can help with?"]
        for ending in generic_endings:
            if cleaned_reply.lower().endswith(ending):
                cleaned_reply = cleaned_reply[:-len(ending)].strip().rstrip(',.!')
                if not cleaned_reply.endswith('.'):
                    cleaned_reply += "..."

        return cleaned_reply if cleaned_reply else raw_reply

    except Exception as e:
        logger.error(f"❌ Ollama Error: {e}")
        return "ERROR: NEURAL LINK TIMEOUT. Is Ollama running?"

def load_brain():
    """Ensures the model is pulled in Ollama."""
    logger.info(f"🧠 Checking if model {settings.GPT_MODEL_ID} is ready in Ollama...")
    pull_url = f"{settings.OLLAMA_HOST}/api/pull"
    try:
        requests.post(pull_url, json={"name": settings.GPT_MODEL_ID}, timeout=5)
    except:
        logger.warning("⚠️ Could not reach Ollama to verify model status.")
