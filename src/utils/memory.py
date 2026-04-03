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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                value TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(category, value)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT,
                status TEXT DEFAULT 'pending',
                project_name TEXT,
                due_date DATETIME,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def add_task(self, task_name, project_name="Portfolio", status="pending", due_date=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO user_tasks (task_name, project_name, status, due_date) VALUES (?, ?, ?, ?)', 
                       (task_name, project_name, status, due_date))
        conn.commit()
        conn.close()

    def get_tasks(self, status=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if status:
            cursor.execute('SELECT task_name, project_name, status, due_date FROM user_tasks WHERE status = ?', (status,))
        else:
            cursor.execute('SELECT task_name, project_name, status, due_date FROM user_tasks')
        tasks = cursor.fetchall()
        conn.close()
        return [{"name": t[0], "project": t[1], "status": t[2], "due": t[3]} for t in tasks]

    def add_message(self, role, content):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO chat_history (role, content) VALUES (?, ?)', (role, content))
        conn.commit()
        conn.close()

    def add_preference(self, category, value):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT OR IGNORE INTO user_preferences (category, value) VALUES (?, ?)', (category, value))
            conn.commit()
        finally:
            conn.close()

    def get_preferences(self, category=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if category:
            cursor.execute('SELECT category, value FROM user_preferences WHERE category = ?', (category,))
        else:
            cursor.execute('SELECT category, value FROM user_preferences')
        
        prefs = cursor.fetchall()
        conn.close()
        return [{"category": category, "value": value} for category, value in prefs]

    def clear_preferences(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM user_preferences')
        conn.commit()
        conn.close()

    def get_recent_history(self, limit=10):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Get the last N messages, then reverse them so they are in chronological order
        cursor.execute('''
            SELECT role, content FROM (
                SELECT * FROM chat_history ORDER BY id DESC LIMIT ?
            ) ORDER BY id ASC
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
