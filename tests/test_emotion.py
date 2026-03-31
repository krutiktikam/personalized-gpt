import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add project root to sys.path if not present
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.emotion.detect import detect_emotion

@pytest.fixture
def mock_classifier():
    with patch("src.emotion.detect.classifier") as mock:
        yield mock

def test_detect_emotion_joy(mock_classifier):
    mock_classifier.return_value = [[{'label': 'joy', 'score': 0.98}]]
    assert detect_emotion("I am so happy!") == "happy"

def test_detect_emotion_sadness(mock_classifier):
    mock_classifier.return_value = [[{'label': 'sadness', 'score': 0.98}]]
    assert detect_emotion("I am so sad...") == "sad"

def test_detect_emotion_anger(mock_classifier):
    mock_classifier.return_value = [[{'label': 'anger', 'score': 0.98}]]
    assert detect_emotion("I am so angry!") == "angry"

def test_detect_emotion_unknown(mock_classifier):
    mock_classifier.return_value = [[{'label': 'unknown', 'score': 0.98}]]
    assert detect_emotion("Something else") == "neutral"

def test_detect_emotion_error(mock_classifier):
    mock_classifier.side_effect = Exception("Test Error")
    assert detect_emotion("Cause error") == "neutral"
