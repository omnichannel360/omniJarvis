"""Google Drive connector — Tier 0 read-only."""
from typing import Any

class DriveConnector:
    """Read-only access to Google Drive."""

    def __init__(self, access_token: str) -> None:
        self.access_token = access_token

    async def find_file(self, name: str) -> dict[str, Any]:
        """Find file by name."""
        return {}

    async def read_file(self, file_id: str) -> str:
        """Read file content."""
        return ""
