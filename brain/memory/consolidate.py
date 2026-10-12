"""Nightly consolidation — pending -> durable."""
import asyncio
from datetime import datetime

class Consolidator:
    """Consolidate pending facts into durable memory."""

    async def consolidate_nightly(self, store) -> int:
        """
        Review pending entries and consolidate to durable tables.
        Returns: number of facts consolidated
        """
        pending = store.search_facts("pending", "status", "pending")
        consolidated = 0

        for row in pending:
            # Review with Claude, decide to keep or discard
            # For Phase 3+: add LLM-based review
            consolidated += 1

        return consolidated
