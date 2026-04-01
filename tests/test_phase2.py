import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.gpt.pipeline import run_pipeline
from src.utils.memory import memory

@pytest.fixture(autouse=True)
def clean_memory():
    memory.clear_memory()
    memory.clear_preferences()
    yield

@patch('src.gpt.pipeline.extract_facts')
@patch('src.gpt.pipeline.generate_response')
@patch('src.gpt.pipeline.detect_emotion')
def test_pipeline_with_facts(mock_detect, mock_generate, mock_extract):
    # Setup mocks
    mock_extract.return_value = [{"category": "hobby", "value": "soccer"}]
    mock_generate.return_value = "That's cool you like soccer!"
    mock_detect.return_value = "neutral"
    
    # Run pipeline
    response = run_pipeline("I love soccer")
    
    # Assertions: Use 'startswith' because personality flavoring appends text
    assert response["reply"].startswith("That's cool you like soccer!")
    
    # Check if fact was stored
    prefs = memory.get_preferences()
    assert len(prefs) == 1
    assert prefs[0]["category"] == "hobby"
    assert prefs[0]["value"] == "soccer"
    
    # Check if generate_response was called with user_facts
    mock_generate.assert_called_once()
    args, kwargs = mock_generate.call_args
    assert "user_facts" in kwargs
    assert kwargs["user_facts"] == prefs

@patch('src.gpt.pipeline.extract_facts')
@patch('src.gpt.pipeline.generate_response')
def test_pipeline_no_facts(mock_generate, mock_extract):
    mock_extract.return_value = []
    mock_generate.return_value = "Hello!"
    
    run_pipeline("Just saying hi")
    
    prefs = memory.get_preferences()
    assert len(prefs) == 0
