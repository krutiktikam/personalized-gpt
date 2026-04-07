import json
import os
import random
import time
import sys
from pathlib import Path

# Add project root to sys.path if not present
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.gpt.generate import generate_response
from src.gpt.extract import extract_facts
from src.emotion.detect import detect_emotion
from src.personality.response import engine
from src.utils.memory import memory
from src.gpt.reflection import generate_proactive_suggestion

from src.gpt.scheduler import plan_work_sprint

def run_pipeline(user_input, mode="default"):
    # 1. Update personality
    engine.set_personality(mode)
    config = engine.get_config()
    
    # 2. Extract and Store User Facts (Skills, Availability, etc.)
    facts = extract_facts(user_input)
    availability_found = None
    new_skill_added = False
    for fact in facts:
        memory.add_preference(fact.get("category"), fact.get("value"))
        if fact.get("category") == "availability":
            availability_found = fact.get("value")
        if fact.get("category") == "skill":
            new_skill_added = True
    
    # 3. Add user message to memory
    memory.add_message("user", user_input)
    
    # 4. Get recent context
    history = memory.get_recent_history(limit=10)
    
    # 5. Get User Facts for Injection
    user_facts = memory.get_preferences()
    
    # 6. Detect Emotion
    emotion = detect_emotion(user_input)
    
    # 7. Generate raw AI response
    # IF the user mentioned availability, let's trigger the scheduler
    if availability_found:
        base_res = plan_work_sprint(availability_found)
    else:
        base_res = generate_response(history, config, emotion=emotion, user_facts=user_facts)
    
    # 8. Check for Proactive Reflection (Local Decision Loop)
    # Trigger if: 
    # - New skill was just added
    # - User asks about next steps/advice
    # - OR 10% random chance if we have skills
    reflection_triggers = ["what next", "next step", "advice", "career", "learn", "suggest"]
    should_reflect = new_skill_added or any(word in user_input.lower() for word in reflection_triggers)
    
    if not should_reflect and random.random() < 0.1: # 10% chance
        should_reflect = True
        
    if should_reflect:
        reflection = generate_proactive_suggestion(user_facts, config)
        if reflection:
            base_res += f"\n\n[Autonomous Reflection]\n{reflection}"
    
    # 9. Apply occasional personality quirks
    flavored_res = engine.shape_response(base_res, emotion)
    
    # 10. Add static prefix for the UI only
    prefix = config.get("prefix", "")
    final_res = f"{prefix}{flavored_res}"
    
    # 11. Save Aura's flavored response to memory (WITHOUT the static prefix)
    memory.add_message("assistant", flavored_res)
    
    # Return both the text and the emotion (for the character)
    return {
        "reply": final_res,
        "emotion": emotion
    }

if __name__ == "__main__":
    # Test for Skills and Scheduling
    test_input = "I'm actually pretty good at React and Python. Tomorrow I'm free from 6 PM to 9 PM, can you help me plan a work schedule for my portfolio?"
    print(f"\n--- TESTING AURA ARCHITECT (Phase 2) ---")
    print(f"Input: {test_input}")
    result = run_pipeline(test_input, mode="default")
    print(f"\nResponse: {result['reply']}")
    print(f"-----------------------------\n")