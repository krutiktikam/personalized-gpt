import json
import os
import random
import time
from src.gpt.generate import generate_response
from src.gpt.extract import extract_facts
from src.emotion.detect import detect_emotion
from src.personality.response import engine
from src.utils.memory import memory

def run_pipeline(user_input, mode="default"):
    # 1. Update personality
    engine.set_personality(mode)
    config = engine.get_config()
    
    # 2. Extract and Store User Facts (Day 3-4)
    facts = extract_facts(user_input)
    for fact in facts:
        memory.add_preference(fact.get("category"), fact.get("value"))
    
    # 3. Add user message to memory
    memory.add_message("user", user_input)
    
    # 4. Get recent context (limit to 10 messages for speed)
    history = memory.get_recent_history(limit=10)
    
    # 5. Get User Facts for Injection (Day 5)
    user_facts = memory.get_preferences()
    
    # 6. Detect Emotion for flavoring AND future animation
    emotion = detect_emotion(user_input)
    
    # 7. Generate raw AI response with Contextual Injection
    base_res = generate_response(history, config, user_facts=user_facts)
    
    # 8. Apply personality flavoring
    final_res = engine.shape_response(base_res, emotion)
    
    # 9. Save Aura's response to memory
    memory.add_message("assistant", final_res)
    
    # Return both the text and the emotion (for the character)
    return {
        "reply": final_res,
        "emotion": emotion
    }

if __name__ == "__main__":
    # Quick test
    print(run_pipeline("I had a really rough day today...", mode="supportive"))