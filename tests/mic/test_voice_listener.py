import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from mic.voice_listener import VoiceListener
import threading
import speech_recognition as sr

class TestVoiceListener:
    @pytest.fixture
    def mock_voice_service(self):
        return MagicMock()

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

    @patch('mic.voice_listener.datetime')
    def test_keyword_activation(self, mock_dt):
        mock_recognizer = MagicMock()
        mock_microphone = MagicMock()
        mock_source = MagicMock()
        mock_audio = MagicMock()

        mock_microphone.__enter__.return_value = mock_source
        mock_recognizer.listen.return_value = mock_audio
        mock_recognizer.recognize_google.return_value = "listen"

        self.listener.recognizer = mock_recognizer
        self.listener.microphone = mock_microphone

        now =  datetime(2025, 7, 19, 12, 0, 0)
        mock_dt.now.return_value = now
        self.listener.listen_for_command()
        expected_stop = now + timedelta(seconds=10)
        assert self.listener.stop_listening_at == expected_stop
        self.voice_service.send_to_publisher.assert_not_called()

    @patch('mic.voice_listener.datetime')
    def test_it_publishes_only_within_window(self, mock_dt):
        now = datetime(2025, 7, 19, 12, 0, 0)
        self.listener.stop_listening_at = now + timedelta(seconds=10)
        mock_dt.now.return_value = now
        mock_recognizer = MagicMock()
        mock_microphone = MagicMock()
        mock_source = MagicMock()
        mock_audio = MagicMock()
        mock_microphone.__enter__.return_value = mock_source
        mock_recognizer.listen.return_value = mock_audio
        mock_recognizer.recognize_google.return_value = "Oi, bop!"
        self.listener.recognizer = mock_recognizer
        self.listener.microphone = mock_microphone
        self.listener.listen_for_command()
        mock_recognizer.recognize_google.assert_called_once_with(mock_audio, language="en-GB")
        self.voice_service.send_to_publisher.assert_called_with("oi, bop!")

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


    @patch('mic.voice_listener.datetime')
    def test_ignores_command_outside_of_listening_window(self, mock_dt):
        now = datetime(2025, 7, 19, 12, 0, 0)
        self.listener.stop_listening_at = now - timedelta(seconds=10)
        mock_dt.now.return_value = now

        mock_recognizer = MagicMock()
        mock_microphone = MagicMock()
        mock_source = MagicMock()
        mock_audio = MagicMock()

        mock_microphone.__enter__.return_value = mock_source
        mock_recognizer.listen.return_value = mock_audio
        mock_recognizer.recognize_google.return_value = "Oi, bop!"
        self.listener.recognizer = mock_recognizer
        self.listener.microphone = mock_microphone
        self.listener.listen_for_command()
        self.voice_service.send_to_publisher.assert_not_called()
