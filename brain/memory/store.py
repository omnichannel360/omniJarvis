"""Memory store — CRUD operations."""
import sqlite3
from pathlib import Path
from typing import Any, Optional, List

class MemoryStore:
    """SQLite memory store."""

    def __init__(self, db_path: str) -> None:
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(db_path)
        self._init_schema()

    def _init_schema(self) -> None:
        """Initialize schema from schema.sql."""
        schema_path = Path(__file__).parent / "schema.sql"
        if schema_path.exists():
            with open(schema_path) as f:
                self.conn.executescript(f.read())

    def add_fact(self, table: str, **kwargs: Any) -> int:
        """Add fact to table."""
        cols = ", ".join(kwargs.keys())
        placeholders = ", ".join("?" * len(kwargs))
        query = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
        cursor = self.conn.execute(query, list(kwargs.values()))
        self.conn.commit()
        return cursor.lastrowid

    def search_facts(self, table: str, key: str, value: Any) -> List[tuple]:
        """Search facts."""
        cursor = self.conn.execute(
            f"SELECT * FROM {table} WHERE {key} = ?", (value,)
        )
        return cursor.fetchall()

    def recall(self, limit: int = 10) -> List[tuple]:
        """Recall recent decisions."""
        cursor = self.conn.execute(
            "SELECT * FROM decisions ORDER BY created_at DESC LIMIT ?", (limit,)
        )
        return cursor.fetchall()
