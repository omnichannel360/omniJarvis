"""Voice pipeline — wake -> VAD -> STT -> send to brain."""
import asyncio
from typing import Optional, Callable

class VoicePipeline:
    """End-to-end voice processing."""

    def __init__(self) -> None:
        self.is_listening = False
        self.on_transcript: Optional[Callable[[str], None]] = None

    async def start(self) -> None:
        """Start listening for wake word."""
        self.is_listening = True

    async def stop(self) -> None:
        """Stop listening."""
        self.is_listening = False

    async def process_audio_stream(self, audio_stream) -> str:
        """
        Process continuous audio stream.
        1. Detect wake word
        2. Detect voice activity
        3. Stream STT
        4. Send transcript to brain
        """
        # Phase 2+: Implement full pipeline
        return ""

    def set_transcript_callback(self, callback: Callable[[str], None]) -> None:
        """Set callback for when transcript arrives."""
        self.on_transcript = callback
