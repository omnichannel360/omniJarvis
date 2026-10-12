"""Kill file sentinel — halts execution before next tool call."""
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

KILL_FILE = Path(r"C:\Jarvis\.JARVIS_STOP")

def is_kill_file_set() -> bool:
    """Check if kill file exists."""
    return KILL_FILE.exists()

def set_kill_file() -> None:
    """Create kill file."""
    KILL_FILE.parent.mkdir(parents=True, exist_ok=True)
    KILL_FILE.touch()
    logger.info("Kill file set")

def clear_kill_file() -> None:
    """Remove kill file."""
    if KILL_FILE.exists():
        KILL_FILE.unlink()
        logger.info("Kill file cleared")
