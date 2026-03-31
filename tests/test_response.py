import pytest
from pathlib import Path
import sys
import json

# Add project root to sys.path if not present
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.personality.response import PersonalityEngine

@pytest.fixture
def mock_personality_json(tmp_path):
    p_path = tmp_path / "personality.json"
    config = {
        "default": {
            "tone": "supportive",
            "traits": ["empathetic"],
            "boredom_level": 0.0,
            "attachment_level": 0.0,
            "prefix": "[SUPPORTIVE] "
        },
        "playful": {
            "tone": "funny",
            "traits": ["humorous"],
            "boredom_level": 1.0, # Always bored for testing
            "attachment_level": 1.0, # Always attached for testing
            "prefix": "[PLAYFUL] "
        }
    }
    p_path.write_text(json.dumps(config))
    return p_path

def test_personality_engine_init(mock_personality_json):
    engine = PersonalityEngine(config_path=mock_personality_json)
    assert engine.current_mode == "default"
    assert engine.get_config()["tone"] == "supportive"

def test_set_personality(mock_personality_json):
    engine = PersonalityEngine(config_path=mock_personality_json)
    engine.set_personality("playful")
    assert engine.current_mode == "playful"
    assert engine.get_config()["tone"] == "funny"
    
    engine.set_personality("invalid")
    assert engine.current_mode == "default"

def test_shape_response_flavor(mock_personality_json):
    engine = PersonalityEngine(config_path=mock_personality_json)
    engine.set_personality("playful")
    
    # In playful mode, boredom and attachment are 1.0, so they should always be added
    response = engine.shape_response("Hello.", "happy")
    assert "That’s wonderful!" in response
    assert "Honestly, I’m kinda bored right now." in response
    assert "You know, I really enjoy talking with you." in response
    assert response.startswith("Hello.")

def test_shape_response_default(mock_personality_json):
    engine = PersonalityEngine(config_path=mock_personality_json)
    # default mode has 0 boredom/attachment
    response = engine.shape_response("Hello.", "neutral")
    assert response == "Hello."
