"""Tests for policy gate."""
import pytest
from policy.tiers import Tier, is_forbidden, get_tier


def test_tier_0_is_read_only():
    """Tier 0 tools are read-only."""
    assert get_tier("file.read") == Tier.TIER_0
    assert get_tier("screenshot") == Tier.TIER_0


def test_tier_1_is_reversible():
    """Tier 1 tools are reversible."""
    assert get_tier("workspace.write") == Tier.TIER_1
    assert get_tier("git.commit") == Tier.TIER_1


def test_tier_2_is_external():
    """Tier 2 tools are external."""
    assert get_tier("mail.send") == Tier.TIER_2
    assert get_tier("github.create_pr") == Tier.TIER_2


def test_tier_3_is_forbidden():
    """Tier 3 tools are forbidden."""
    assert is_forbidden("payment.process")
    assert is_forbidden("password.read")
    assert is_forbidden("account.delete")
    assert is_forbidden("security.disable")


def test_tier_3_refusal_not_overridable():
    """Tier 3 refusal is hard-coded, not configurable."""
    # If the gate check ever returns True for Tier 3, this breaks
    forbidden_tools = [
        "payment.process",
        "password.read",
        "credentials.access",
        "account.delete",
        "security.disable",
    ]
    for tool in forbidden_tools:
        assert is_forbidden(tool), f"{tool} should be forbidden"


def test_unknown_tool_defaults_to_tier_2():
    """Unknown tools default to Tier 2 (ask first)."""
    assert get_tier("unknown.tool") == Tier.TIER_2


def test_gate_check_allows_tier_0(gate):
    """Gate allows Tier 0 tools."""
    allowed, reason = gate.check("file.read")
    assert allowed
    assert "Approved" in reason


def test_gate_check_refuses_tier_3(gate):
    """Gate refuses Tier 3 tools."""
    allowed, reason = gate.check("payment.process")
    assert not allowed
    assert "forbidden" in reason.lower()


def test_gate_logs_audit(gate):
    """Gate logs audit entries."""
    gate.check("file.read")
    assert gate.audit_log_path.exists()
    logs = gate.audit_log_path.read_text().strip().split("\n")
    assert len(logs) >= 1
