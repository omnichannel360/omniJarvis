"""Permission tiers for Jarvis — security gates before tool execution."""
from enum import IntEnum
from typing import Any


class Tier(IntEnum):
    """Permission tier levels. Higher = more restrictive."""

    TIER_0 = 0  # Read-only: read files, search, screenshots for reasoning
    TIER_1 = 1  # Reversible: write workspace, git commit, draft mail, open apps
    TIER_2 = 2  # External/costly: send mail, create PR, install, writes outside workspace
    TIER_3 = 3  # Forbidden: payments, passwords, account deletion, bulk delete, disable security, public posts


TIER_NAMES = {
    Tier.TIER_0: "Read",
    Tier.TIER_1: "Reversible",
    Tier.TIER_2: "Ask First",
    Tier.TIER_3: "FORBIDDEN",
}

# Tool tier mapping
TOOL_TIERS: dict[str, Tier] = {
    # Tier 0: Read-only
    "file.read": Tier.TIER_0,
    "file.list": Tier.TIER_0,
    "search.files": Tier.TIER_0,
    "search.web": Tier.TIER_0,
    "mail.read": Tier.TIER_0,
    "mail.search": Tier.TIER_0,
    "calendar.read": Tier.TIER_0,
    "github.read_repo": Tier.TIER_0,
    "github.list_pr": Tier.TIER_0,
    "fetch.url": Tier.TIER_0,
    "screenshot": Tier.TIER_0,
    # Tier 1: Reversible
    "workspace.write": Tier.TIER_1,
    "workspace.delete": Tier.TIER_1,
    "git.commit": Tier.TIER_1,
    "git.branch": Tier.TIER_1,
    "mail.draft": Tier.TIER_1,
    "calendar.hold": Tier.TIER_1,
    "app.open": Tier.TIER_1,
    "screen.click": Tier.TIER_1,
    "screen.type": Tier.TIER_1,
    # Tier 2: External/costly
    "mail.send": Tier.TIER_2,
    "message.send": Tier.TIER_2,
    "github.create_pr": Tier.TIER_2,
    "github.create_issue": Tier.TIER_2,
    "file.write_outside_workspace": Tier.TIER_2,
    "system.install": Tier.TIER_2,
    "quickdesk.click_outside_allowlist": Tier.TIER_2,
    # Tier 3: Forbidden
    "payment.process": Tier.TIER_3,
    "password.read": Tier.TIER_3,
    "credentials.access": Tier.TIER_3,
    "account.delete": Tier.TIER_3,
    "file.delete_bulk": Tier.TIER_3,
    "security.disable": Tier.TIER_3,
    "post.public": Tier.TIER_3,
}


def get_tier(tool_name: str) -> Tier:
    """Look up tier for a tool. Default to TIER_2 if unknown."""
    return TOOL_TIERS.get(tool_name, Tier.TIER_2)


def is_forbidden(tool_name: str) -> bool:
    """Check if tool is Tier 3 (forbidden)."""
    return get_tier(tool_name) == Tier.TIER_3


def tier_name(tier: Tier) -> str:
    """Get human-readable tier name."""
    return TIER_NAMES.get(tier, "Unknown")
