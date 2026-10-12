"""Alerting — email/Telegram on anomalies."""

class AlertManager:
    """Send alerts on system anomalies."""

    async def check_and_alert(self, monitor) -> None:
        """
        Check system health, send alerts if thresholds exceeded.
        - CPU > 80%
        - Memory > 85%
        - Daily cost > $50
        """
        # Phase 4+: Check metrics, send via Telegram
        pass

    async def send_alert(self, level: str, message: str) -> None:
        """Send alert (critical, warning, info)."""
        # Phase 4+: Telegram notification
        pass
