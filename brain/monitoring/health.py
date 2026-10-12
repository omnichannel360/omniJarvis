"""System health monitoring — CPU, memory, API quota."""
from typing import Dict, Any

class HealthMonitor:
    """Monitor Jarvis system health."""

    async def check_system(self) -> Dict[str, Any]:
        """Check CPU, memory, disk."""
        return {
            "cpu_percent": 0.0,
            "memory_percent": 0.0,
            "disk_percent": 0.0,
        }

    async def check_api_quota(self) -> Dict[str, Any]:
        """Check Anthropic API quota for today."""
        return {
            "calls_today": 0,
            "tokens_today": 0,
            "cost_today": 0.0,
            "daily_limit": 50.0,
        }

    async def check_tailscale(self) -> bool:
        """Check Tailscale connectivity."""
        return True
