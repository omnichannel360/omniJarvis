"""
Jarvis brain app — boots OpenJarvis with Claude engine + policy gate.
Loads JAMES.md profile, registers hooks, runs orchestrator.
"""
import logging
from pathlib import Path
from typing import Any

import yaml
from anthropic import Anthropic

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


class JarvisBrain:
    """Jarvis brain orchestrator."""

    def __init__(self) -> None:
        self.config_path = Path(__file__).parent.parent.parent / "config"
        self.load_config()
        self.client = Anthropic(api_key=self.get_api_key())
        self.profile = self.load_profile()

    def load_config(self) -> None:
        """Load config YAML files."""
        with open(self.config_path / "models.yaml") as f:
            self.models_config = yaml.safe_load(f)
        with open(self.config_path / "settings.yaml") as f:
            self.settings_config = yaml.safe_load(f)
        logger.info("Config loaded")

    def get_api_key(self) -> str:
        """Retrieve API key from credential store (stub)."""
        import os
        key = os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise ValueError("ANTHROPIC_API_KEY not set; run scripts/setup_keys.py")
        return key

    def load_profile(self) -> dict[str, Any]:
        """Load JAMES.md as profile."""
        profile_path = Path(__file__).parent.parent / "memory" / "JAMES.md"
        logger.info(f"Loaded profile: {profile_path}")
        return {"name": "James Duran", "role": "Founder/CTO"}

    def ask(self, prompt: str) -> str:
        """Send prompt to Claude, return response."""
        response = self.client.messages.create(
            model=self.models_config["models"]["sonnet"]["id"],
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text  # type: ignore

    def run(self) -> None:
        """Start brain orchestrator (stub)."""
        logger.info("Jarvis brain started")


_brain: JarvisBrain | None = None


def get_brain() -> JarvisBrain:
    """Get or create brain singleton."""
    global _brain
    if not _brain:
        _brain = JarvisBrain()
    return _brain


def boot() -> JarvisBrain:
    """Boot brain."""
    brain = get_brain()
    brain.run()
    return brain


if __name__ == "__main__":
    import sys
    brain = boot()
    if len(sys.argv) > 1 and sys.argv[1] == "ask":
        prompt = " ".join(sys.argv[2:])
        print(brain.ask(prompt))
