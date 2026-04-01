import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import os
import sys
from pathlib import Path

# Add project root to sys.path if not present
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from config.settings import settings

# --- AUTHENTICATION ---
HF_TOKEN = settings.HF_TOKEN
model_id = settings.GPT_MODEL_ID

from src.utils.logger import logger

# 4-bit configuration for your RTX 3050 (4GB)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True
)

# Global placeholders for the model and tokenizer
model = None
tokenizer = None

def load_brain():
    global model, tokenizer
    if model is not None:
        return

    logger.info(f"🚀 Loading Aura's Enhanced Brain ({model_id})...")

    tokenizer = AutoTokenizer.from_pretrained(model_id, token=HF_TOKEN)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="auto",
        token=HF_TOKEN
    )

def generate_response(history: list, personality_config: dict, user_facts: list = None):
    # Ensure model is loaded before use
    load_brain()

    # System Prompt tells the model how to act
    system_msg = (
        f"You are Aura, a quirky AI companion. "
        f"Current Mood: {personality_config.get('tone')}. "
        f"Traits: {', '.join(personality_config.get('traits', []))}."
    )
    
    # Inject known facts about the user
    if user_facts:
        facts_str = "; ".join([f"{f['category']}: {f['value']}" for f in user_facts])
        system_msg += f" Known info about user: {facts_str}."

    # Prepend the system message to the history
    messages = [{"role": "system", "content": system_msg}] + history

    # Apply template and generate mask
    model_inputs = tokenizer.apply_chat_template(
        messages, 
        add_generation_prompt=True, 
        return_dict=True, # Explicitly return a dict
        return_tensors="pt"
    ).to(model.device)

    # Use torch.no_grad() to save memory
    with torch.no_grad():
        outputs = model.generate(
            **model_inputs, # Pass the entire dict (input_ids + attention_mask)
            max_new_tokens=120, 
            temperature=0.8,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id
        )

    # Extract response
    response_ids = outputs[0][model_inputs['input_ids'].shape[-1]:]
    response_text = tokenizer.decode(response_ids, skip_special_tokens=True).strip()

    # Memory cleanup for small GPUs
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    prefix = personality_config.get("prefix", "")
    return f"{prefix}{response_text}"