"""Text-to-speech — Kokoro 82M (local, no cloud)."""
from pathlib import Path

class TTSEngine:
    """Local TTS via Kokoro."""

    def __init__(self) -> None:
        self.voice = "ava"  # Default voice
        self.speed = 1.0

    def synthesize(self, text: str, output_path: Path) -> bool:
        """
        Synthesize text to speech.
        Returns: True if successful
        """
        # Phase 2+: Load Kokoro model, generate audio
        # For now: stub
        return True

    def stream(self, text: str):
        """
        Stream audio chunks as they generate.
        Yields: audio chunks (PCM bytes)
        """
        # Phase 2+: Stream TTS output
        yield b""
