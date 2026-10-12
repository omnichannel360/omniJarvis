"""Tier promotion system — Tier 2 to Tier 1 after 14 days + 10 successes."""
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import json

class PromotionTracker:
    """Track tier promotions over time."""

    def __init__(self, log_path: str) -> None:
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def can_promote(self, tool_name: str, days: int = 14, successes: int = 10) -> bool:
        """Check if tool can be promoted from Tier 2 to 1."""
        if not self.log_path.exists():
            return False

        lines = self.log_path.read_text().strip().split("\n")
        entries = [json.loads(line) for line in lines if line]

        # Filter to this tool's successes
        tool_successes = [
            e for e in entries
            if e.get("tool") == tool_name and e.get("allowed") and e.get("tier") == "Ask First"
        ]

        if len(tool_successes) < successes:
            return False

        # Check if oldest success is older than 14 days
        oldest = min(
            datetime.fromisoformat(e["timestamp"]) for e in tool_successes
        )
        return datetime.utcnow() - oldest >= timedelta(days=days)

    def record_promotion(self, tool_name: str, promoted_to: int) -> None:
        """Record promotion decision."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "tool": tool_name,
            "promoted_to_tier": promoted_to,
        }
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
