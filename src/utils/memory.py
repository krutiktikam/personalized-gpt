import psycopg2
import logging
import sys
import datetime
from pathlib import Path

# Add project root to sys.path if not present
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from config.settings import settings

logger = logging.getLogger(__name__)

class ConversationMemory:
    def __init__(self, db_url=settings.DATABASE_URL):
        self.db_url = db_url
        self.is_connected = False
        # Volatile in-memory fallback
        self._temp_history = []
        self._temp_prefs = []
        self._temp_tasks = []
        
        try:
            self._init_db()
            self.is_connected = True
            logger.info("✅ Connected to PostgreSQL database.")
        except Exception as e:
            logger.warning(f"⚠️ PostgreSQL not available: {e}. Falling back to volatile in-memory storage.")

    def _get_connection(self):
        return psycopg2.connect(self.db_url)

    def _init_db(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                role TEXT,
                content TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id SERIAL PRIMARY KEY,
                category TEXT,
                value TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(category, value)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_tasks (
                id SERIAL PRIMARY KEY,
                task_name TEXT,
                status TEXT DEFAULT 'pending',
                project_name TEXT,
                due_date TIMESTAMP,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def add_task(self, task_name, project_name="Portfolio", status="pending", due_date=None):
        if not self.is_connected:
            self._temp_tasks.append({
                "name": task_name, 
                "project": project_name, 
                "status": status, 
                "due": due_date
            })
            return
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO user_tasks (task_name, project_name, status, due_date) VALUES (%s, %s, %s, %s)', 
                           (task_name, project_name, status, due_date))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error adding task: {e}")

    def get_tasks(self, status=None):
        if not self.is_connected:
            if status:
                return [t for t in self._temp_tasks if t["status"] == status]
            return self._temp_tasks
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            if status:
                cursor.execute('SELECT task_name, project_name, status, due_date FROM user_tasks WHERE status = %s', (status,))
            else:
                cursor.execute('SELECT task_name, project_name, status, due_date FROM user_tasks')
            tasks = cursor.fetchall()
            conn.close()
            return [{"name": t[0], "project": t[1], "status": t[2], "due": t[3]} for t in tasks]
        except Exception as e:
            logger.error(f"Error getting tasks: {e}")
            return []

    def add_message(self, role, content):
        if not self.is_connected:
            self._temp_history.append({"role": role, "content": content})
            return
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO chat_history (role, content) VALUES (%s, %s)', (role, content))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error adding message: {e}")

    def add_preference(self, category, value):
        if not self.is_connected:
            # Check for duplicates in memory
            if not any(p["category"] == category and p["value"] == value for p in self._temp_prefs):
                self._temp_prefs.append({"category": category, "value": value})
            return
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO user_preferences (category, value) VALUES (%s, %s) ON CONFLICT (category, value) DO NOTHING', (category, value))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error adding preference: {e}")

    def get_preferences(self, category=None):
        if not self.is_connected:
            if category:
                return [p for p in self._temp_prefs if p["category"] == category]
            return self._temp_prefs
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            if category:
                cursor.execute('SELECT category, value FROM user_preferences WHERE category = %s', (category,))
            else:
                cursor.execute('SELECT category, value FROM user_preferences')
            
            prefs = cursor.fetchall()
            conn.close()
            return [{"category": category, "value": value} for category, value in prefs]
        except Exception as e:
            logger.error(f"Error getting preferences: {e}")
            return []

    def clear_preferences(self):
        if not self.is_connected:
            self._temp_prefs = []
            return
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM user_preferences')
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error clearing preferences: {e}")

    def get_recent_history(self, limit=10):
        if not self.is_connected:
            return self._temp_history[-limit:]
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT role, content FROM (
                    SELECT * FROM chat_history ORDER BY id DESC LIMIT %s
                ) sub ORDER BY id ASC
            ''', (limit,))
            history = cursor.fetchall()
            conn.close()
            return [{"role": role, "content": content} for role, content in history]
        except Exception as e:
            logger.error(f"Error getting history: {e}")
            return []

    def clear_memory(self):
        if not self.is_connected:
            self._temp_history = []
            return
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM chat_history')
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error clearing memory: {e}")

# Singleton instance
memory = ConversationMemory()
