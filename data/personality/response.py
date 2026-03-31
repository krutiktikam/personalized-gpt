import json

# Load personality traits from traits.json
with open("src/personality/traits.json", "r") as f:
    personality = json.load(f)

def shape_response(base_response: str, emotion: str) -> str:
    traits = personality["traits"]

    if emotion == "joy" and traits.get("empathetic"):
        return f"😊 I'm glad to hear that! {base_response}"
    elif emotion == "sadness" and traits.get("empathetic"):
        return f"💙 I understand this feels tough. {base_response}"
    elif emotion == "anger" and traits.get("empathetic"):
        return f"😤 I hear your frustration. {base_response}"
    else:
        return base_response