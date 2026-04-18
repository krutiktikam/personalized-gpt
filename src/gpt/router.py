import requests
import json
from src.utils.logger import logger
from config.settings import settings
from src.gpt.tool_handler import TOOL_DESCRIPTIONS

def route_task(user_input, mode="default"):
    """
    Decides which model size to use based on task complexity.
    Returns: 'small' (3B) or 'large' (7B+)
    """
    complex_keywords = [
        "architect", "design", "scalable", "optimize", "refactor", 
        "security", "review", "complex", "system", "infrastructure"
    ]
    
    # Force large for specific modes
    if mode in ["architect", "review"]:
        logger.info(f"🧠 Routing to LARGE model due to mode: {mode}")
        return "large"
        
    # Check for complexity in input
    if any(kw in user_input.lower() for kw in complex_keywords) or len(user_input.split()) > 50:
        logger.info("🧠 Routing to LARGE model due to task complexity.")
        return "large"
        
    logger.info("⚡ Routing to SMALL model for quick response.")
    return "small"

def determine_tool_use(user_input):
    """
    Asks the LLM to output a tool call ONLY if needed.
    """
    tools_str = "\n".join([f"- {t['name']}: {t['description']} (Params: {t['parameters']})" for t in TOOL_DESCRIPTIONS])
    
    prompt = f"""
[SYSTEM]
You are a strict Tool Dispatcher.
Available Tools:
{tools_str}

If the user wants to create a folder, create a file, list files, or get system status, you MUST output the call in this format:
<call tool="tool_name">{{"param": "value"}}</call>

If no tool is needed for the user's request, output exactly: NONE

[USER]
{user_input}

[OUTPUT]
"""
    
    payload = {
        "model": settings.GPT_MODEL_ID,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.0, "stop": ["\n"]}
    }
    
    try:
        response = requests.post(f"{settings.OLLAMA_HOST}/api/generate", json=payload, timeout=10)
        res = response.json().get("response", "").strip()
        logger.info(f"🔍 Tool Router Output: {res}")
        return res if "<call" in res else None
    except Exception as e:
        logger.error(f"Tool Routing Error: {e}")
        return None
