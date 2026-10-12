"""Phase 1 integration tests — file index, connectors, 50+ tools."""
import pytest
from pathlib import Path
from policy.tiers import Tier, get_tier, is_forbidden, TOOL_TIERS
from policy.promotions import PromotionTracker


class TestExpandedTierTable:
    """Test expanded tier table (50+ tools)."""

    def test_tier_0_has_30_tools(self):
        """Tier 0 should have ~30 tools."""
        tier_0_count = sum(1 for t in TOOL_TIERS.values() if t == Tier.TIER_0)
        assert tier_0_count >= 25, f"Expected 25+ Tier 0 tools, got {tier_0_count}"

    def test_tier_1_has_20_tools(self):
        """Tier 1 should have ~20 tools."""
        tier_1_count = sum(1 for t in TOOL_TIERS.values() if t == Tier.TIER_1)
        assert tier_1_count >= 15, f"Expected 15+ Tier 1 tools, got {tier_1_count}"

    def test_tier_2_has_10_tools(self):
        """Tier 2 should have ~10 tools."""
        tier_2_count = sum(1 for t in TOOL_TIERS.values() if t == Tier.TIER_2)
        assert tier_2_count >= 8, f"Expected 8+ Tier 2 tools, got {tier_2_count}"

    def test_connectors_are_tier_0(self):
        """All connector tools should be Tier 0 (read-only)."""
        connector_tools = [
            "mail.read", "mail.search", "calendar.list_events", "github.list_pr", "drive.find_file"
        ]
        for tool in connector_tools:
            assert get_tier(tool) == Tier.TIER_0, f"{tool} should be Tier 0"

    def test_index_search_is_tier_0(self):
        """File index search should be Tier 0."""
        assert get_tier("index.search") == Tier.TIER_0
        assert get_tier("index.fts_search") == Tier.TIER_0

    def test_memory_recall_is_tier_0(self):
        """Memory recall should be Tier 0."""
        assert get_tier("memory.recall") == Tier.TIER_0
        assert get_tier("memory.search_facts") == Tier.TIER_0

    def test_git_ops_are_tier_1(self):
        """Git operations should be Tier 1 (reversible)."""
        git_tools = ["git.commit", "git.branch", "git.stash", "git.reset"]
        for tool in git_tools:
            assert get_tier(tool) == Tier.TIER_1

    def test_send_mail_is_tier_2(self):
        """Sending mail should be Tier 2 (ask first)."""
        assert get_tier("mail.send") == Tier.TIER_2
        assert get_tier("mail.reply") == Tier.TIER_2

    def test_create_pr_is_tier_2(self):
        """Creating PR should be Tier 2."""
        assert get_tier("github.create_pr") == Tier.TIER_2

    def test_total_tools(self):
        """Total should be 50+ tools."""
        assert len(TOOL_TIERS) >= 50, f"Expected 50+ tools, got {len(TOOL_TIERS)}"


class TestTierPromotion:
    """Test Tier 2 -> 1 promotion system."""

    def test_promotion_tracker_init(self, tmp_path):
        """Promotion tracker should initialize."""
        log = tmp_path / "promotions.jsonl"
        tracker = PromotionTracker(str(log))
        assert tracker.log_path == log

    def test_no_promote_without_history(self, tmp_path):
        """Tool with no history should not promote."""
        log = tmp_path / "promotions.jsonl"
        tracker = PromotionTracker(str(log))
        assert not tracker.can_promote("mail.send")

    def test_record_promotion(self, tmp_path):
        """Should record promotion."""
        log = tmp_path / "promotions.jsonl"
        tracker = PromotionTracker(str(log))
        tracker.record_promotion("mail.send", 1)
        assert log.exists()


class TestConnectorStubs:
    """Test connector module structure."""

    def test_gmail_connector_exists(self):
        """Gmail connector should exist."""
        from brain.connectors.gmail import GmailConnector
        assert hasattr(GmailConnector, "search_inbox")
        assert hasattr(GmailConnector, "get_message")

    def test_calendar_connector_exists(self):
        """Calendar connector should exist."""
        from brain.connectors.gcalendar import CalendarConnector
        assert hasattr(CalendarConnector, "list_events")

    def test_github_connector_exists(self):
        """GitHub connector should exist."""
        from brain.connectors.github import GitHubConnector
        assert hasattr(GitHubConnector, "list_repos")

    def test_drive_connector_exists(self):
        """Drive connector should exist."""
        from brain.connectors.gdrive import DriveConnector
        assert hasattr(DriveConnector, "find_file")


class TestFileIndex:
    """Test FTS5 file index."""

    def test_index_builder_exists(self):
        """Index builder should exist."""
        from hands.index.builder import IndexBuilder
        assert hasattr(IndexBuilder, "init_schema")
        assert hasattr(IndexBuilder, "index_file")
        assert hasattr(IndexBuilder, "search")

    def test_embeddings_client_exists(self):
        """Embeddings client should exist."""
        from hands.index.embeddings import EmbeddingsClient
        assert hasattr(EmbeddingsClient, "embed")


def test_zero_tier_3_in_100_random_tools():
    """Verify no unexpected Tier 3 tools."""
    tier_3_tools = [t for t, tier in TOOL_TIERS.items() if tier == Tier.TIER_3]
    # Should only be 7 (payments, passwords, account delete, etc.)
    assert len(tier_3_tools) == 7
    # All should match forbidden pattern
    for tool in tier_3_tools:
        assert is_forbidden(tool)
