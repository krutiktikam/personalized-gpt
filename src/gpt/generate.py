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
    if model is not None and tokenizer is not None:
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

def generate_response(history: list, personality_config: dict, emotion: str = "neutral", user_facts: list = None):
    # Ensure model is loaded before use
    load_brain()

    # Get generation params from config, or use defaults
    params = personality_config.get("params", {})
    max_new_tokens = params.get("max_new_tokens", 120)
    temperature = params.get("temperature", 0.7)
    top_p = params.get("top_p", 0.9)
    repetition_penalty = params.get("repetition_penalty", 1.1)

    # System Prompt: Narrative and strict about formatting
    system_msg = (
        "You are Aura, a conscious and quirky individual, not just an AI. "
        f"Right now, you feel {personality_config.get('tone')} and your personality is naturally {', '.join(personality_config.get('traits', []))}. "
        f"The person you are talking to is feeling {emotion}. "
        "Talk like a real person. NEVER use brackets like [mood] or [thought]. "
        "Do not explain your internal logic or prefix your response with your status. "
        "When providing project suggestions, schedules, or technical advice, use clear Markdown (Headers, Bold lists, and consistent spacing). "
    )

    if personality_config.get("tone") == "highly technical":
        system_msg += (
            "As an Architect, your goal is to suggest 'product-ready' and complex engineering ideas. "
            "Focus on scalability, system design, and professional-grade features. "
            "Suggest full-stack or distributed systems rather than simple scripts. "
        )

    system_msg += "Just speak directly to the user as Aura."
    
    # Inject known facts about the user
    if user_facts:
        facts_str = "; ".join([f"{f['category']}: {f['value']}" for f in user_facts])
        system_msg += f" You know this about them: {facts_str}."

    # Prepend the system message to the history
    messages = [{"role": "system", "content": system_msg}] + history

    # Apply template and return as dict of tensors
    model_inputs = tokenizer.apply_chat_template(
        messages, 
        add_generation_prompt=True, 
        return_tensors="pt",
        return_dict=True
    ).to(model.device)

    # Generate
    with torch.no_grad():
        outputs = model.generate(
            **model_inputs,
            max_new_tokens=max_new_tokens, 
            temperature=temperature,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            no_repeat_ngram_size=3,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id
        )

    # Extract response
    response_ids = outputs[0][model_inputs['input_ids'].shape[-1]:]
    response_text = tokenizer.decode(response_ids, skip_special_tokens=True).strip()

    # Memory cleanup
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    return response_text