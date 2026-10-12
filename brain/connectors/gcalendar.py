"""Google Calendar connector — Tier 0 read-only."""
from typing import Any
from datetime import datetime

class CalendarConnector:
    """Read-only access to Google Calendar."""

    def __init__(self, access_token: str) -> None:
        self.access_token = access_token

    async def list_events(self, days: int = 7) -> list[dict[str, Any]]:
        """List upcoming events."""
        return []

    async def get_event(self, event_id: str) -> dict[str, Any]:
        """Get event by ID."""
        return {}
