import json
import os
import random
import time
from src.gpt.generate import generate_response
from src.emotion.detect import detect_emotion
from src.personality.response import engine
from src.utils.memory import memory

def run_pipeline(user_input, mode="default"):
    # 1. Update personality
    engine.set_personality(mode)
    config = engine.get_config()
    
    # 2. Add user message to memory
    memory.add_message("user", user_input)
    
    # 3. Get recent context (limit to 10 messages for speed)
    history = memory.get_recent_history(limit=10)
    
    # 4. Detect Emotion for flavoring AND future animation
    emotion = detect_emotion(user_input)
    
    # 5. Generate raw AI response
    base_res = generate_response(history, config)
    
    # 6. Apply personality flavoring
    final_res = engine.shape_response(base_res, emotion)
    
    # 7. Save Aura's response to memory
    memory.add_message("assistant", final_res)
    
    # Return both the text and the emotion (for the character)
    return {
        "reply": final_res,
        "emotion": emotion
    }

if __name__ == "__main__":
    # Quick test
    print(run_pipeline("I had a really rough day today...", mode="supportive"))