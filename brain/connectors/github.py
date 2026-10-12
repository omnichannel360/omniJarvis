"""GitHub connector — Tier 0 read-only."""
from typing import Any

class GitHubConnector:
    """Read-only access to GitHub."""

    def __init__(self, access_token: str) -> None:
        self.access_token = access_token

    async def list_repos(self) -> list[str]:
        """List user repos."""
        return []

    async def search_issues(self, query: str) -> list[dict[str, Any]]:
        """Search issues."""
        return []

    async def get_notifications(self) -> list[dict[str, Any]]:
        """Get notifications."""
        return []
