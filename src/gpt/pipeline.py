import json
import os
import random
import time
import sys
import asyncio
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
from src.gpt.router import route_task

from src.gpt.scheduler import plan_work_sprint

async def run_pipeline(user_input, mode="default"):
    # 0. Check for explicit mode overrides
    if "/review" in user_input.lower():
        mode = "review"
        user_input = user_input.replace("/review", "").strip()
    elif "/architect" in user_input.lower():
        mode = "architect"
        user_input = user_input.replace("/architect", "").strip()

    # 0b. Route task complexity
    task_size = await asyncio.to_thread(route_task, user_input, mode)
    # In a real multi-GPU setup, we'd pass task_size to generate_response
    
    # 1. Update personality
    engine.set_personality(mode)
    config = engine.get_config()
    
    # 2. Extract and Store User Facts (Skills, Availability, etc.)
    # We strip code blocks for extraction to prevent hallucinations/false availability triggers
    import re
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
        import re
        snippets = re.findall(r"```(?:\w+)?\n(.*?)\n```", user_input, re.DOTALL)
        for snippet in snippets:
            if len(snippet.strip()) > 20:
                await asyncio.to_thread(vector_store.add_snippet, snippet.strip(), metadata={"source": "user_chat"})
    
    # 3. Add user message to memory
    await asyncio.to_thread(memory.add_message, "user", user_input)
    
    # 4. Get recent context - Reduce to 6 to keep it focused
    history = await asyncio.to_thread(memory.get_recent_history, 6)
    
    # 5. Get User Facts for Injection
    user_facts = await asyncio.to_thread(memory.get_preferences)
    
    # 5b. RAG: Query for relevant context
    rag_context = []
    # Query docs for general knowledge
    docs_context = await asyncio.to_thread(vector_store.query_docs, user_input, n_results=2)
    rag_context.extend(docs_context)
    # Query snippets for past user code
    snippets_context = await asyncio.to_thread(vector_store.query_snippets, user_input, n_results=2)
    rag_context.extend(snippets_context)
    
    # 6. Detect Emotion
    emotion = await asyncio.to_thread(detect_emotion, user_input)
    
    # 7. Generate raw AI response (Multi-turn tool loop)
    if availability_found:
        base_res = await asyncio.to_thread(plan_work_sprint, availability_found)
    else:
        # Loop for tool use
        max_tool_depth = 2
        current_depth = 0
        base_res = await asyncio.to_thread(
            generate_response, 
            history=history, 
            personality_config=config, 
            emotion=emotion, 
            user_facts=user_facts, 
            context=rag_context
        )
        
        while current_depth < max_tool_depth:
            tool_results = await asyncio.to_thread(process_tool_calls, base_res)
            if not tool_results:
                break
                
            # Add tool call and its result to history for the next turn
            history.append({"role": "assistant", "content": base_res})
            history.append({"role": "system", "content": f"TOOL_EXECUTION_RESULTS:\n" + "\n".join(tool_results)})
            
            # Generate new response with tool output
            base_res = await asyncio.to_thread(
            generate_response, 
            history=history, 
            personality_config=config, 
            emotion=emotion, 
            user_facts=user_facts, 
            context=rag_context
        )
            current_depth += 1
    
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
        reflection = await asyncio.to_thread(generate_proactive_suggestion, user_facts, config)
        if reflection:
            print(f"DEBUG: Integrating reflection: {reflection[:50]}...")
            # Integrate reflection naturally without the bot-like header
            base_res += f"\n\nThinking ahead... {reflection}"
    
    # 9. Apply occasional personality quirks
    flavored_res = engine.shape_response(base_res, emotion)
    
    # 10. Add static prefix for the UI only
    prefix = config.get("prefix", "")
    final_res = f"{prefix}{flavored_res}"
    
    # 11. Save Aura's flavored response to memory (WITHOUT the static prefix)
    await asyncio.to_thread(memory.add_message, "assistant", flavored_res)
    
    # Return both the text and the emotion (for the character)
    return {
        "reply": final_res,
        "emotion": emotion
    }

if __name__ == "__main__":
    # Test for Skills and Scheduling
    async def main():
        test_input = "I'm actually pretty good at React and Python. Tomorrow I'm free from 6 PM to 9 PM, can you help me plan a work schedule for my portfolio?"
        print(f"\n--- TESTING AURA ARCHITECT (Phase 2) ---")
        print(f"Input: {test_input}")
        result = await run_pipeline(test_input, mode="default")
        print(f"\nResponse: {result['reply']}")
        print(f"-----------------------------\n")
    
    asyncio.run(main())