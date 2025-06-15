# tests/conftest.py
import pytest
from unittest.mock import MagicMock, patch

@pytest.fixture(autouse=True, scope="session")
def mock_sr_microphone_and_recognizer():
    with patch("speech_recognition.Microphone", MagicMock()), \
         patch("speech_recognition.Recognizer", MagicMock()):
        yield
