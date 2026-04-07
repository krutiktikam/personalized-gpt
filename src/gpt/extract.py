import torch
import json
import re
import src.gpt.generate as gen
from src.utils.logger import logger

def extract_facts(user_input):
    """
    Extracts personal facts from user input using the LLM.
    Returns a list of dicts: [{"category": "...", "value": "..."}]
    """
    gen.load_brain()
    
    if gen.tokenizer is None or gen.model is None:
        logger.error("Failed to load tokenizer or model for fact extraction.")
        return []

    system_msg = (
        "Extract personal facts from the user's message. Focus on: "
        "- 'skill': technologies or tools they know (e.g. React, Python) "
        "- 'availability': when they are free to work (e.g. tomorrow 6pm, weekend) "
        "- 'goal': what they want to achieve (e.g. build a portfolio, learn CSS) "
        "- 'preference': general likes/dislikes. "
        "Output ONLY a JSON list of objects with 'category' and 'value'. "
        "Example: [{\"category\": \"skill\", \"value\": \"TypeScript\"}]. "
        "If no relevant facts are found, output []."
    )

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_input}
    ]

    try:
        model_inputs = gen.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt"
        ).to(gen.model.device)

        with torch.no_grad():
            outputs = gen.model.generate(
                **model_inputs,
                max_new_tokens=100,
                do_sample=False,
                pad_token_id=gen.tokenizer.pad_token_id
            )

        response_ids = outputs[0][model_inputs['input_ids'].shape[-1]:]
        response_text = gen.tokenizer.decode(response_ids, skip_special_tokens=True).strip()

        # Try to find JSON in the response
        # Use a non-greedy regex to find the first [ ] block
        match = re.search(r'\[.*?\]', response_text, re.DOTALL)
        if match:
            facts = json.loads(match.group(0))
            if isinstance(facts, list):
                return facts
        return []
    except Exception as e:
        logger.error(f"Error during fact extraction: {e}")
        return []

if __name__ == "__main__":
    # Test (requires model to be loaded)
    test_input = "My name is Krutik and I love playing soccer."
    print(f"Input: {test_input}")
    print(f"Extracted: {extract_facts(test_input)}")
