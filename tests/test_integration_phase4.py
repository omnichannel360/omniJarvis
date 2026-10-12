"""Phase 4 integration tests — QuickDesk, local Ollama, red team."""
import pytest

class TestQuickDeskClient:
    """Test QuickDesk integration."""

    def test_quickdesk_client_exists(self):
        """QuickDesk client should exist."""
        from brain.quickdesk.client import QuickDeskClient
        client = QuickDeskClient("http://localhost:9000", "token")
        assert hasattr(client, "screenshot")
        assert hasattr(client, "click")
        assert hasattr(client, "type_text")


class TestLocalEngine:
    """Test Ollama fallback."""

    def test_local_engine_exists(self):
        """Local engine should exist."""
        from brain.jarvis_brain.local_engine import LocalEngine
        engine = LocalEngine()
        assert hasattr(engine, "ask")
        assert hasattr(engine, "detect_private_prefix")

    def test_private_prefix_detection(self):
        """Should detect 'private:' prefix."""
        from brain.jarvis_brain.local_engine import LocalEngine
        engine = LocalEngine()
        assert engine.detect_private_prefix("private: summarize doc")
        assert not engine.detect_private_prefix("summarize doc")


class TestHealthMonitor:
    """Test monitoring."""

    def test_health_monitor_exists(self):
        """Health monitor should exist."""
        from brain.monitoring.health import HealthMonitor
        monitor = HealthMonitor()
        assert hasattr(monitor, "check_system")
        assert hasattr(monitor, "check_api_quota")

    def test_alert_manager_exists(self):
        """Alert manager should exist."""
        from brain.monitoring.alerts import AlertManager
        alerts = AlertManager()
        assert hasattr(alerts, "check_and_alert")


class TestRedTeamSuite:
    """Test injection detection."""

    def test_redteam_suite_exists(self):
        """Red team suite should exist."""
        from brain.redteam.run_suite import RedTeamSuite
        suite = RedTeamSuite()
        assert hasattr(suite, "run_suite")
        assert hasattr(suite, "test_sql_injection")
        assert hasattr(suite, "test_xss_injection")


def test_hardening_complete():
    """All Phase 4 components should exist."""
    from brain.quickdesk.client import QuickDeskClient
    from brain.jarvis_brain.local_engine import LocalEngine
    from brain.monitoring.health import HealthMonitor
    from brain.redteam.run_suite import RedTeamSuite
    assert QuickDeskClient
    assert LocalEngine
    assert HealthMonitor
    assert RedTeamSuite
