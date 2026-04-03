import torch
import json
import re
import src.gpt.generate as gen
from src.utils.memory import memory
from src.utils.logger import logger

def plan_work_sprint(availability, focus_area="Portfolio"):
    """
    Generates a step-by-step schedule for the user based on their free time.
    """
    gen.load_brain()
    
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
        "Keep the tone encouraging but professional. Suggest specific project ideas if they have no tasks."
    )

    prompt = f"I am free at these times: {availability}. Create a schedule for me."

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": prompt}
    ]

    try:
        # Use slightly more tokens for a full schedule
        model_inputs = gen.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt"
        ).to(gen.model.device)

        with torch.no_grad():
            outputs = gen.model.generate(
                **model_inputs,
                max_new_tokens=300, 
                temperature=0.7,
                do_sample=True,
                pad_token_id=gen.tokenizer.pad_token_id
            )

        response_ids = outputs[0][model_inputs['input_ids'].shape[-1]:]
        plan = gen.tokenizer.decode(response_ids, skip_special_tokens=True).strip()
        return plan
    except Exception as e:
        logger.error(f"Error during scheduling: {e}")
        return "I'm sorry, I couldn't generate a schedule right now. Let's try again."

if __name__ == "__main__":
    # Test
    print(plan_work_sprint("Tomorrow from 6 PM to 9 PM"))