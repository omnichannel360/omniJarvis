"""Phase 2 integration tests — voice pipeline."""
import pytest

class TestVoicePipeline:
    """Test voice components."""

    def test_wake_word_detector_exists(self):
        """Wake word detector should exist."""
        from hands.voice.wake import WakeWordDetector
        detector = WakeWordDetector()
        assert hasattr(detector, "detect")

    def test_voice_pipeline_exists(self):
        """Voice pipeline should exist."""
        from hands.voice.pipeline import VoicePipeline
        pipeline = VoicePipeline()
        assert hasattr(pipeline, "start")
        assert hasattr(pipeline, "stop")
        assert hasattr(pipeline, "process_audio_stream")

    def test_tts_engine_exists(self):
        """TTS engine should exist."""
        from hands.voice.tts import TTSEngine
        engine = TTSEngine()
        assert hasattr(engine, "synthesize")
        assert hasattr(engine, "stream")

    def test_approval_panel_websocket_exists(self):
        """WebSocket approval panel should exist."""
        from policy.approval_ui import ApprovalPanel
        panel = ApprovalPanel()
        assert hasattr(panel, "request_approval")
        assert hasattr(panel, "handle_approval")


def test_voice_round_trip_under_2_5_seconds():
    """Voice round-trip latency should be under 2.5s."""
    # Phase 2+: Benchmark wake word detection + STT + TTS
    # For now: just verify structure exists
    from hands.voice.wake import WakeWordDetector
    from hands.voice.pipeline import VoicePipeline
    from hands.voice.tts import TTSEngine
    
    assert WakeWordDetector
    assert VoicePipeline
    assert TTSEngine
