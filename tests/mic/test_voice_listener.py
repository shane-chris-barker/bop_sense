import pytest
from unittest.mock import MagicMock
from mic.voice_listener import VoiceListener
import threading
import speech_recognition as sr


class TestVoiceListener:
    @pytest.fixture
    def mock_voice_service(self):
        return MagicMock()

    @pytest.fixture
    def voice_listener(self, mock_voice_service):
        return VoiceListener(mock_voice_service)
    
    @pytest.fixture(autouse=True)
    def setup(self, mock_voice_service):
        self.voice_service = mock_voice_service
        self.listener = VoiceListener(self.voice_service)

    def test_start_sets_running_and_starts_thread(self):
        self.listener._continuous_listen = MagicMock()
        self.listener.start()
        assert self.listener.running is True
        assert self.listener.listener_thread is not None
        assert isinstance(self.listener.listener_thread, threading.Thread)
        self.listener.stop()

    def test_stop_stops_thread(self):
        self.listener.running = True
        self.listener.listener_thread = threading.Thread(target=lambda: None)
        self.listener.listener_thread.start()
        self.listener.stop()
        assert self.listener.running is False
        assert not self.listener.listener_thread.is_alive()

    def test_listen_for_command_success(self):
        mock_recognizer = MagicMock()
        mock_microphone = MagicMock()
        mock_source = MagicMock()
        mock_audio = MagicMock()

        mock_microphone.__enter__.return_value = mock_source
        mock_recognizer.listen.return_value = mock_audio
        mock_recognizer.recognize_google.return_value = "hello bop"

        self.listener.recognizer = mock_recognizer
        self.listener.microphone = mock_microphone

        self.listener.listen_for_command()

        mock_recognizer.adjust_for_ambient_noise.assert_called_once_with(mock_source)
        mock_recognizer.listen.assert_called_once_with(mock_source)
        mock_recognizer.recognize_google.assert_called_once_with(mock_audio)
        self.voice_service.send_to_publisher.assert_called_once_with("hello bop")

    def test_listen_for_command_unknown_value_error(self, caplog):
        mock_recognizer = MagicMock()
        mock_microphone = MagicMock()
        mock_source = MagicMock()

        mock_microphone.__enter__.return_value = mock_source
        mock_recognizer.listen.return_value = MagicMock()
        mock_recognizer.recognize_google.side_effect = sr.UnknownValueError

        self.listener.recognizer = mock_recognizer
        self.listener.microphone = mock_microphone

        with caplog.at_level('DEBUG'):
            self.listener.listen_for_command()

        self.voice_service.send_to_publisher.assert_not_called()
        assert any("not sure what you said" in msg for msg in caplog.messages)
