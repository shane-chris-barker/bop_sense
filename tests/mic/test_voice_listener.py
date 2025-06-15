import pytest
from unittest.mock import patch, MagicMock
from mic.voice_listener import VoiceListener
import threading
import speech_recognition as sr


class TestVoiceListener:
    mic_patch = 'mic.voice_listener.sr.Microphone'
    recognizer_patch = 'mic.voice_listener.sr.Recognizer'
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

    @patch(mic_patch)
    @patch(recognizer_patch)
    def test_listen_for_command_success(self, mock_recognizer_class, mock_microphone_class):
        # Setup mocks
        mock_microphone = MagicMock()
        mock_microphone_class.return_value = mock_microphone
        mock_source = MagicMock()
        mock_microphone.__enter__.return_value = mock_source

        mock_recognizer = MagicMock()
        mock_recognizer_class.return_value = mock_recognizer
        mock_audio = MagicMock()
        mock_recognizer.listen.return_value = mock_audio
        mock_recognizer.recognize_google.return_value = "hello bop"

        # Mock voice service
        mock_voice_service = MagicMock()
        listener = VoiceListener(mock_voice_service)

        listener.listen_for_command()

        mock_recognizer.adjust_for_ambient_noise.assert_called_once_with(mock_source)
        mock_recognizer.listen.assert_called_once_with(mock_source)
        mock_recognizer.recognize_google.assert_called_once_with(mock_audio)
        mock_voice_service.send_to_publisher.assert_called_once_with("hello bop")

    @patch(mic_patch)
    @patch(recognizer_patch)
    def test_listen_for_command_unknown_value_error(self, mock_microphone, mock_recognizer, caplog):
        mock_source = MagicMock()
        mock_microphone.return_value.__enter__.return_value = mock_source
        recognizer_instance = mock_recognizer.return_value
        recognizer_instance.recognize_google.side_effect = sr.UnknownValueError
        self.listener.recognizer = recognizer_instance
        self.listener.microphone = mock_microphone.return_value

        with caplog.at_level('DEBUG'):
            self.listener.listen_for_command()
        self.voice_service.send_to_publisher.assert_not_called()
        assert any("not sure what you said" in msg for msg in caplog.messages) 