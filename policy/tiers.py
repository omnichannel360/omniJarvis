"""Expanded tier table (50+ tools)."""
from enum import IntEnum

class Tier(IntEnum):
    TIER_0 = 0
    TIER_1 = 1
    TIER_2 = 2
    TIER_3 = 3

TOOL_TIERS = {
    # Tier 0: Read-only (30 tools)
    "file.read": Tier.TIER_0,
    "file.list": Tier.TIER_0,
    "file.stat": Tier.TIER_0,
    "search.files": Tier.TIER_0,
    "search.web": Tier.TIER_0,
    "mail.read": Tier.TIER_0,
    "mail.search": Tier.TIER_0,
    "mail.list_labels": Tier.TIER_0,
    "calendar.read": Tier.TIER_0,
    "calendar.list_events": Tier.TIER_0,
    "calendar.get_event": Tier.TIER_0,
    "github.read_repo": Tier.TIER_0,
    "github.list_pr": Tier.TIER_0,
    "github.search_issues": Tier.TIER_0,
    "github.get_notifications": Tier.TIER_0,
    "drive.find_file": Tier.TIER_0,
    "drive.read_file": Tier.TIER_0,
    "fetch.url": Tier.TIER_0,
    "fetch.allowlisted_domain": Tier.TIER_0,
    "screenshot": Tier.TIER_0,
    "screenshot.window": Tier.TIER_0,
    "index.search": Tier.TIER_0,
    "index.fts_search": Tier.TIER_0,
    "memory.recall": Tier.TIER_0,
    "memory.search_facts": Tier.TIER_0,
    "workspace.list": Tier.TIER_0,
    "workspace.read": Tier.TIER_0,
    "app.list_running": Tier.TIER_0,
    "app.get_info": Tier.TIER_0,
    # Tier 1: Reversible (20 tools)
    "workspace.write": Tier.TIER_1,
    "workspace.create": Tier.TIER_1,
    "workspace.delete": Tier.TIER_1,
    "workspace.move": Tier.TIER_1,
    "git.commit": Tier.TIER_1,
    "git.branch": Tier.TIER_1,
    "git.stash": Tier.TIER_1,
    "git.reset": Tier.TIER_1,
    "mail.draft": Tier.TIER_1,
    "mail.mark_read": Tier.TIER_1,
    "calendar.hold": Tier.TIER_1,
    "calendar.tentative": Tier.TIER_1,
    "app.open": Tier.TIER_1,
    "app.close": Tier.TIER_1,
    "screen.click": Tier.TIER_1,
    "screen.type": Tier.TIER_1,
    "screen.hotkey": Tier.TIER_1,
    "memory.add_fact": Tier.TIER_1,
    "memory.update_fact": Tier.TIER_1,
    # Tier 2: External (10 tools)
    "mail.send": Tier.TIER_2,
    "mail.reply": Tier.TIER_2,
    "message.send": Tier.TIER_2,
    "github.create_pr": Tier.TIER_2,
    "github.create_issue": Tier.TIER_2,
    "github.comment": Tier.TIER_2,
    "file.write_outside_workspace": Tier.TIER_2,
    "system.install": Tier.TIER_2,
    "quickdesk.click_outside_allowlist": Tier.TIER_2,
    "calendar.accept": Tier.TIER_2,
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
    return TOOL_TIERS.get(tool_name, Tier.TIER_2)

def is_forbidden(tool_name: str) -> bool:
    return get_tier(tool_name) == Tier.TIER_3
