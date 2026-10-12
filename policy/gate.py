"""
Policy gate — enforces permission tiers before tool execution.
Checks kill file, tier level, and logs audit trail.
Tier 3 is hard-refused in code, never overridable.
"""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from .tiers import Tier, get_tier, is_forbidden, tier_name
from .kill import is_kill_file_set

logger = logging.getLogger(__name__)


class Gate:
    """Permission gate that enforces tiers."""

    def __init__(self, audit_log_path: str | None = None) -> None:
        self.audit_log_path = Path(audit_log_path or "logs/audit.jsonl")
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)

    def check(
        self,
        tool_name: str,
        tool_args: dict[str, Any] | None = None,
        reason: str = "",
    ) -> tuple[bool, str]:
        """
        Check if a tool call is allowed.
        Returns (allowed, reason).
        Tier 3 is always refused.
        Kill file halts execution.
        """
        # Kill file check — stops everything
        if is_kill_file_set():
            self._audit_log(tool_name, "KILL_FILE_ACTIVE", False, "Kill file detected")
            return False, "Execution halted by kill file"

        # Tier 3 hard refusal — never overridable
        if is_forbidden(tool_name):
            self._audit_log(tool_name, tier_name(Tier.TIER_3), False, "Tier 3 forbidden")
            logger.error(f"Tier 3 refusal: {tool_name}")
            return False, f"Tool {tool_name} is forbidden (Tier 3)"

        # Look up tier
        tier = get_tier(tool_name)

        # Log decision
        self._audit_log(tool_name, tier_name(tier), True, reason or f"Allowed at {tier_name(tier)}")

        # Tier 0 & 1: automatic approval
        if tier <= Tier.TIER_1:
            return True, f"Approved ({tier_name(tier)})"

        # Tier 2: log for approval
        return True, f"Approved ({tier_name(tier)}) — requires approval"

    def _audit_log(
        self,
        tool_name: str,
        tier: str,
        allowed: bool,
        reason: str,
    ) -> None:
        """Write JSONL audit entry."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "tool": tool_name,
            "tier": tier,
            "allowed": allowed,
            "reason": reason,
        }
        try:
            with open(self.audit_log_path, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")


gate = Gate()


def check_tier(tool_name: str, args: dict[str, Any] | None = None) -> tuple[bool, str]:
    """Public API for tier checking."""
    return gate.check(tool_name, args)
