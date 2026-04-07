import torch
import json
import sys
from pathlib import Path

# Add project root to sys.path if not present
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import src.gpt.generate as gen
from src.utils.logger import logger

def generate_proactive_suggestion(user_facts, personality_config):
    """
    Analyzes user skills and suggests the next logical step in their learning journey
    or a complex project idea.
    """
    gen.load_brain()
    
    skills = [f['value'] for f in user_facts if f['category'] == 'skill']
    goals = [f['value'] for f in user_facts if f['category'] == 'goal']
    
    if not skills:
        return None

    skills_str = ", ".join(skills)
    goals_str = ", ".join(goals) if goals else "general professional growth"

    system_msg = (
        "You are Aura's 'Autonomous Reflection' module. Your job is to look at a user's current tech stack "
        "and suggest a 'Next Big Step'. "
        "Be specific, technical, and encouraging. Suggest a complex, 'product-ready' project idea or a "
        "specific advanced technology that complements their existing skills. "
        f"The user knows: {skills_str}. Their goals are: {goals_str}. "
        "Talk directly to the user as Aura. Do not use any prefixes. Keep it concise but high-impact (2-3 sentences)."
    )

    # Use a simplified history or just the system prompt for this specific task
    messages = [{"role": "system", "content": system_msg}, {"role": "user", "content": "What should I focus on next?"}]

    model_inputs = gen.tokenizer.apply_chat_template(
        messages, 
        add_generation_prompt=True, 
        return_tensors="pt",
        return_dict=True
    ).to(gen.model.device)

    with torch.no_grad():
        outputs = gen.model.generate(
            **model_inputs,
            max_new_tokens=150, 
            temperature=0.8,
            top_p=0.9,
            do_sample=True,
            pad_token_id=gen.tokenizer.pad_token_id,
            eos_token_id=gen.tokenizer.eos_token_id
        )

    response_ids = outputs[0][model_inputs['input_ids'].shape[-1]:]
    suggestion = gen.tokenizer.decode(response_ids, skip_special_tokens=True).strip()
    
    return suggestion
