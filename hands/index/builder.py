"""File index builder — FTS5 + embeddings."""
import sqlite3
from pathlib import Path
from typing import Generator

class IndexBuilder:
    """Build FTS5 index over workspace files."""

    def __init__(self, db_path: str) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path)

    def init_schema(self) -> None:
        """Create FTS5 table."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS files_fts (
                id INTEGER PRIMARY KEY,
                path TEXT UNIQUE NOT NULL,
                content TEXT NOT NULL,
                embedding BLOB
            )
        """)
        self.conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS fts_content USING fts5(
                path, content
            )
        """)
        self.conn.commit()

    def index_file(self, path: Path, content: str) -> None:
        """Add file to index."""
        try:
            self.conn.execute(
                "INSERT OR REPLACE INTO files_fts (path, content) VALUES (?, ?)",
                (str(path), content)
            )
            self.conn.execute(
                "INSERT OR REPLACE INTO fts_content (path, content) VALUES (?, ?)",
                (str(path), content)
            )
            self.conn.commit()
        except Exception as e:
            print(f"Index error: {e}")

    def rebuild(self, workspace: Path) -> int:
        """Rebuild index from workspace."""
        count = 0
        for file_path in workspace.rglob("*"):
            if file_path.is_file() and not file_path.name.startswith("."):
                try:
                    content = file_path.read_text(errors="ignore")
                    self.index_file(file_path, content)
                    count += 1
                except Exception:
                    pass
        return count

    def search(self, query: str, limit: int = 10) -> list[tuple[str, str]]:
        """Search FTS5 index."""
        cursor = self.conn.execute(
            "SELECT path, content FROM fts_content WHERE fts_content MATCH ? LIMIT ?",
            (query, limit)
        )
        return cursor.fetchall()
