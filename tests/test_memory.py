import pytest
import psycopg2
import os
from pathlib import Path
import sys

# Add project root to sys.path if not present
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.utils.memory import ConversationMemory
from config.settings import settings

# Skip these tests if PostgreSQL is not available
def is_postgres_available():
    try:
        conn = psycopg2.connect(settings.DATABASE_URL)
        conn.close()
        return True
    except:
        return False

pytestmark = pytest.mark.skipif(not is_postgres_available(), reason="PostgreSQL not available")

@pytest.fixture
def memory():
    # Use the default settings URL but we could point to a test DB here
    mem = ConversationMemory(db_url=settings.DATABASE_URL)
    # Clear tables before each test
    conn = mem._get_connection()
    cursor = conn.cursor()
    cursor.execute("TRUNCATE chat_history, user_preferences, user_tasks RESTART IDENTITY CASCADE")
    conn.commit()
    conn.close()
    return mem

def test_init_db(memory):
    conn = memory._get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name='chat_history'")
    assert cursor.fetchone() is not None
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name='user_preferences'")
    assert cursor.fetchone() is not None
    conn.close()

def test_preferences(memory):
    memory.add_preference("hobby", "soccer")
    memory.add_preference("hobby", "chess")
    memory.add_preference("name", "Alice")
    
    # Test getting all
    prefs = memory.get_preferences()
    assert len(prefs) == 3
    
    # Test getting by category
    hobbies = memory.get_preferences(category="hobby")
    assert len(hobbies) == 2
    assert any(p["value"] == "soccer" for p in hobbies)
    assert any(p["value"] == "chess" for p in hobbies)
    
    # Test unique constraint (Postgres ON CONFLICT handled in code)
    memory.add_preference("hobby", "soccer")
    prefs = memory.get_preferences(category="hobby")
    assert len(prefs) == 2
    
    # Test clear
    memory.clear_preferences()
    assert len(memory.get_preferences()) == 0

def test_add_and_get_history(memory):
    memory.add_message("user", "Hello")
    memory.add_message("assistant", "Hi there!")
    
    history = memory.get_recent_history(limit=10)
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "Hello"
    assert history[1]["role"] == "assistant"
    assert history[1]["content"] == "Hi there!"

def test_get_recent_history_limit(memory):
    for i in range(15):
        memory.add_message("user", f"Msg {i}")
    
    history = memory.get_recent_history(limit=5)
    assert len(history) == 5
    assert history[0]["content"] == "Msg 10"
    assert history[-1]["content"] == "Msg 14"

def test_clear_memory(memory):
    memory.add_message("user", "Hello")
    memory.clear_memory()
    
    history = memory.get_recent_history()
    assert len(history) == 0
