import sqlite3
import json
import os
import sys
from pathlib import Path

# Add project root to sys.path if not present
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from config.settings import settings

class ConversationMemory:
    def __init__(self, db_path=settings.MEMORY_DB_PATH):
        self.db_path = str(db_path)
        self._init_db()

    def _init_db(self):
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                role TEXT,
                content TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def add_message(self, role, content):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO chat_history (role, content) VALUES (?, ?)', (role, content))
        conn.commit()
        conn.close()

    def get_recent_history(self, limit=10):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Get the last N messages, then reverse them so they are in chronological order
        cursor.execute('''
            SELECT role, content FROM (
                SELECT * FROM chat_history ORDER BY timestamp DESC LIMIT ?
            ) ORDER BY timestamp ASC
        ''', (limit,))
        history = cursor.fetchall()
        conn.close()
        
        # Convert to list of dicts for easier use with Llama chat templates
        return [{"role": role, "content": content} for role, content in history]

    def clear_memory(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM chat_history')
        conn.commit()
        conn.close()

# Singleton instance
memory = ConversationMemory()
