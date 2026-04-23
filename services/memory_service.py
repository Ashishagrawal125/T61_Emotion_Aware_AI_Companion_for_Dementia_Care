# Handles patient memory storage using SQLite
import sqlite3
from pathlib import Path

class MemoryService:
    def __init__(self, db_path: str = "data/clara_memory.db"):
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_name TEXT NOT NULL,
                    memory_key TEXT NOT NULL,
                    memory_value TEXT NOT NULL
                )
                """
            )

    def save_memory(self, patient_name: str, memory_key: str, memory_value: str):
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO memories (patient_name, memory_key, memory_value) VALUES (?, ?, ?)",
                (patient_name, memory_key, memory_value),
            )

    def get_memories(self, patient_name: str):
        with self._connect() as conn:
            cur = conn.execute(
                "SELECT memory_key, memory_value FROM memories WHERE patient_name = ?",
                (patient_name,),
            )
            return [{"key": row[0], "value": row[1]} for row in cur.fetchall()]
