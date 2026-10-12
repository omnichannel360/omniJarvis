"""Gmail connector — Tier 0 read-only."""
from typing import Any

class GmailConnector:
    """Read-only access to Gmail."""

    def __init__(self, access_token: str) -> None:
        self.access_token = access_token

    async def search_inbox(self, query: str, max_results: int = 10) -> list[dict[str, Any]]:
        """Search inbox."""
        # Phase 1: stub. Phase 2: implement via gmail.py library
        return []

    async def get_message(self, message_id: str) -> dict[str, Any]:
        """Get message by ID."""
        return {}

    async def list_labels(self) -> list[str]:
        """List all labels."""
        return []
