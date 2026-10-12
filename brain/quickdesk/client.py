"""QuickDesk MCP client — remote screen control."""

class QuickDeskClient:
    """Connect to QuickDesk for unattended screen control."""

    def __init__(self, signaling_url: str, device_token: str) -> None:
        self.signaling_url = signaling_url
        self.device_token = device_token

    async def screenshot(self) -> bytes:
        """Capture screenshot."""
        # Phase 4+: Connect to QuickDesk MCP, call screenshot tool
        return b""

    async def click(self, x: int, y: int) -> bool:
        """Click at x, y (Tier 1 if in allowlist, Tier 2 otherwise)."""
        # Phase 4+: Verify app allowlist, execute click
        return True

    async def type_text(self, text: str) -> bool:
        """Type text."""
        # Phase 4+: Execute via QuickDesk
        return True

    async def find_element(self, query: str) -> dict:
        """Find UI element by OCR/accessibility."""
        # Phase 4+: Use QuickDesk structured search
        return {}
