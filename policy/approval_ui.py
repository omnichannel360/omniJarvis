"""WebSocket-based approval UI for Tier 2 tasks."""
import asyncio
from typing import Callable
from datetime import datetime, timedelta


class ApprovalPanel:
    """Tier 2 approval via WebSocket UI."""

    def __init__(self) -> None:
        self.pending_approvals = {}
        self.approval_timeout = timedelta(minutes=10)

    async def request_approval(
        self,
        task_id: str,
        task_name: str,
        details: str,
        ws_send: Callable,
    ) -> bool:
        """Request approval via UI panel."""
        self.pending_approvals[task_id] = {
            "name": task_name,
            "details": details,
            "created": datetime.utcnow(),
        }

        await ws_send({
            "type": "approval_request",
            "task_id": task_id,
            "task": task_name,
            "details": details,
            "expires_in_seconds": 600,
        })

        start = datetime.utcnow()
        while datetime.utcnow() - start < self.approval_timeout:
            if task_id in self.pending_approvals:
                result = self.pending_approvals[task_id].get("approved")
                if result is not None:
                    del self.pending_approvals[task_id]
                    return result
            await asyncio.sleep(0.5)

        if task_id in self.pending_approvals:
            del self.pending_approvals[task_id]
        return False

    async def handle_approval(self, task_id: str, approved: bool) -> None:
        """Handle UI approval/deny."""
        if task_id in self.pending_approvals:
            self.pending_approvals[task_id]["approved"] = approved
