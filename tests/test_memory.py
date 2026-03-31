import pytest
import sqlite3
import os
from pathlib import Path
import sys

# Add project root to sys.path if not present
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.utils.memory import ConversationMemory

@pytest.fixture
def temp_db(tmp_path):
    db_path = tmp_path / "test_memory.db"
    return str(db_path)

def test_init_db(temp_db):
    memory = ConversationMemory(db_path=temp_db)
    assert os.path.exists(temp_db)
    
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='chat_history'")
    assert cursor.fetchone() is not None
    conn.close()

def test_add_and_get_history(temp_db):
    memory = ConversationMemory(db_path=temp_db)
    memory.add_message("user", "Hello")
    memory.add_message("assistant", "Hi there!")
    
    history = memory.get_recent_history(limit=10)
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "Hello"
    assert history[1]["role"] == "assistant"
    assert history[1]["content"] == "Hi there!"

def test_get_recent_history_limit(temp_db):
    memory = ConversationMemory(db_path=temp_db)
    for i in range(15):
        memory.add_message("user", f"Msg {i}")
    
    history = memory.get_recent_history(limit=5)
    assert len(history) == 5
    assert history[0]["content"] == "Msg 10"
    assert history[-1]["content"] == "Msg 14"

def test_clear_memory(temp_db):
    memory = ConversationMemory(db_path=temp_db)
    memory.add_message("user", "Hello")
    memory.clear_memory()
    
    history = memory.get_recent_history()
    assert len(history) == 0
