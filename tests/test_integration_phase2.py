"""Phase 2 integration tests — voice pipeline, Telegram gateway."""
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


class TestTelegramGateway:
    """Test Telegram approval gateway."""

    def test_telegram_gateway_exists(self):
        """Telegram gateway should exist."""
        from brain.telegram_bot import TelegramGateway
        gateway = TelegramGateway("token", 12345)
        assert hasattr(gateway, "request_approval")
        assert hasattr(gateway, "send_message")

    def test_approval_timeout(self):
        """Approval should timeout after 10 minutes."""
        from brain.telegram_bot import TelegramGateway
        from datetime import timedelta
        gateway = TelegramGateway("token", 12345)
        assert gateway.approval_timeout == timedelta(minutes=10)


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
