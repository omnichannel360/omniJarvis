"""Wake word detection — openWakeWord."""
import numpy as np
from typing import Optional

class WakeWordDetector:
    """Detect 'Hey Jarvis' wake word."""

    def __init__(self, model_path: str = "hey_jarvis") -> None:
        self.model_path = model_path
        self.threshold = 0.5

    def detect(self, audio_chunk: np.ndarray) -> bool:
        """
        Detect wake word in audio chunk.
        audio_chunk: 16kHz mono audio as numpy array
        Returns: True if wake word detected
        """
        # Phase 2+: Load openWakeWord model, run inference
        # For now: stub
        return False

    def set_threshold(self, threshold: float) -> None:
        """Adjust detection threshold (0.0-1.0)."""
        self.threshold = threshold
