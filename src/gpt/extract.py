import torch
import json
import re
from src.gpt.generate import model, tokenizer, load_brain
from src.utils.logger import logger

def extract_facts(user_input):
    """
    Extracts personal facts from user input using the LLM.
    Returns a list of dicts: [{"category": "...", "value": "..."}]
    """
    load_brain()
    system_msg = (
        "Extract personal facts (name, hobby, occupation, preference) from the user's message. "
        "Output ONLY a JSON list of objects with 'category' and 'value'. "
        "Example: [{\"category\": \"hobby\", \"value\": \"soccer\"}]. "
        "If no facts are found, output []."
    )

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_input}
    ]

    model_inputs = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_dict=True,
        return_tensors="pt"
    ).to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **model_inputs,
            max_new_tokens=50,
            do_sample=False,
            pad_token_id=tokenizer.pad_token_id
        )

    response_ids = outputs[0][model_inputs['input_ids'].shape[-1]:]
    response_text = tokenizer.decode(response_ids, skip_special_tokens=True).strip()

    # Try to find JSON in the response
    try:
        # Simple regex to find the first [ ] block
        match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if match:
            facts = json.loads(match.group(0))
            if isinstance(facts, list):
                return facts
        return []
    except Exception as e:
        logger.error(f"Failed to parse facts from response: {response_text}. Error: {e}")
        return []

if __name__ == "__main__":
    # Test (requires model to be loaded)
    test_input = "My name is Krutik and I love playing soccer."
    print(f"Input: {test_input}")
    print(f"Extracted: {extract_facts(test_input)}")
