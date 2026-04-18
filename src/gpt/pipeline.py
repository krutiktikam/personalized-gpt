import json
import os
import random
import time
import sys
import asyncio
import re
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
from src.utils.vector_store import vector_store
from src.gpt.tool_handler import process_tool_calls
from src.gpt.router import route_task, determine_tool_use

from src.gpt.scheduler import plan_work_sprint

async def run_pipeline(user_input, mode="default"):
    # 0. Check for explicit mode overrides
    if "/review" in user_input.lower():
        mode = "review"
        user_input = user_input.replace("/review", "").strip()
    elif "/architect" in user_input.lower():
        mode = "architect"
        user_input = user_input.replace("/architect", "").strip()

    # 0c. Explicit Tool Check (Intercept intent before conversation)
    # This prevents the LLM from hallucinating terminal commands in chat
    tool_call = await asyncio.to_thread(determine_tool_use, user_input)
    initial_tool_results = []
    if tool_call:
        res = await asyncio.to_thread(process_tool_calls, tool_call)
        if res:
            initial_tool_results.extend(res)
            # Add to history immediately so the conversation knows it happened
            await asyncio.to_thread(memory.add_message, "system", f"TOOL_EXECUTION_RESULTS:\n" + "\n".join(res))

    # 0b. Route task complexity
    task_size = await asyncio.to_thread(route_task, user_input, mode)
    
    # 1. Update personality
    engine.set_personality(mode)
    config = engine.get_config()
    
    # 2. Extract and Store User Facts
    clean_input_for_extraction = re.sub(r"```.*?```", "", user_input, flags=re.DOTALL)
    facts = await asyncio.to_thread(extract_facts, clean_input_for_extraction)
    availability_found = None
    new_skill_added = False
    for fact in facts:
        await asyncio.to_thread(memory.add_preference, fact.get("category"), fact.get("value"))
        if fact.get("category") == "availability":
            availability_found = fact.get("value")
        if fact.get("category") == "skill":
            new_skill_added = True
            
    # 2b. RAG: Index code snippets if detected
    if "```" in user_input:
        snippets = re.findall(r"```(?:\w+)?\n(.*?)\n```", user_input, re.DOTALL)
        for snippet in snippets:
            if len(snippet.strip()) > 20:
                await asyncio.to_thread(vector_store.add_snippet, snippet.strip(), metadata={"source": "user_chat"})
    
    # 3. Add user message to memory
    await asyncio.to_thread(memory.add_message, "user", user_input)
    
    # 4. Get recent context
    history = await asyncio.to_thread(memory.get_recent_history, 6)
    
    # 5. Get User Facts for Injection
    user_facts = await asyncio.to_thread(memory.get_preferences)
    
    # 5b. RAG: Query for relevant context
    rag_context = []
    docs_context = await asyncio.to_thread(vector_store.query_docs, user_input, n_results=2)
    rag_context.extend(docs_context)
    snippets_context = await asyncio.to_thread(vector_store.query_snippets, user_input, n_results=2)
    rag_context.extend(snippets_context)
    
    # 6. Detect Emotion
    emotion = await asyncio.to_thread(detect_emotion, user_input)
    
    # 7. Generate raw AI response
    if availability_found:
        base_res = await asyncio.to_thread(plan_work_sprint, availability_found)
    else:
        # Conversation with Tool Results integrated into History
        base_res = await asyncio.to_thread(
            generate_response, 
            history=history, 
            personality_config=config, 
            emotion=emotion, 
            user_facts=user_facts, 
            context=rag_context
        )
    
    # 8. Check for Proactive Reflection
    reflection_triggers = ["what next", "next step", "advice", "career", "learn", "suggest"]
    should_reflect = new_skill_added or any(word in user_input.lower() for word in reflection_triggers)
    
    if not should_reflect and random.random() < 0.1: # 10% chance
        should_reflect = True
        
    if should_reflect:
        reflection = await asyncio.to_thread(generate_proactive_suggestion, user_facts, config)
        if reflection:
            base_res += f"\n\nThinking ahead... {reflection}"
    
    # 9. Apply occasional personality quirks
    flavored_res = engine.shape_response(base_res, emotion)
    
    # 10. Add static prefix for the UI only
    prefix = config.get("prefix", "")
    final_res = f"{prefix}{flavored_res}"
    
    # 11. Save Aura's flavored response to memory
    await asyncio.to_thread(memory.add_message, "assistant", flavored_res)
    
    return {
        "reply": final_res,
        "emotion": emotion
    }
