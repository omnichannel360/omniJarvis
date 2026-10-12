"""Local Ollama tier — offline/private execution."""
from typing import Optional

class LocalEngine:
    """Fallback Ollama engine for offline mode."""

    def __init__(self, base_url: str = "http://localhost:11434") -> None:
        self.base_url = base_url
        self.model = "gemma2"  # or qwen, q4 quantized

    async def ask(self, prompt: str) -> str:
        """
        Ask question locally.
        Returns: response from local model
        """
        # Phase 4+: Call Ollama API
        return ""

    def detect_private_prefix(self, prompt: str) -> bool:
        """Detect 'private:' prefix for local-only execution."""
        return prompt.strip().startswith("private:")

    async def execute_private(self, prompt: str) -> str:
        """Execute local-only task."""
        if not self.detect_private_prefix(prompt):
            raise ValueError("Not marked private")
        clean_prompt = prompt.replace("private:", "").strip()
        return await self.ask(clean_prompt)
