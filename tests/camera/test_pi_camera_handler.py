import unittest
from unittest.mock import Mock, patch, MagicMock
import threading
import time
from camera.pi_camera_handler import PiCameraHandler

class TestPiCameraHandler(unittest.TestCase):

    def setUp(self):
        self.mock_publisher = Mock()
        self.picamera2_patcher = patch('camera.pi_camera_handler.Picamera2', MagicMock())
        self.mock_picamera2_class = self.picamera2_patcher.start()
        self.mock_picamera2 = self.mock_picamera2_class.return_value
        self.mock_picamera2.create_still_configuration.return_value = {"mock": "config"}
        self.mock_picamera2.configure = Mock()
        self.mock_picamera2.start = Mock()
        self.mock_picamera2.close = Mock()

    def tearDown(self):
        self.picamera2_patcher.stop()

    def test_initialization(self):
        handler = PiCameraHandler(self.mock_publisher)
        self.mock_picamera2.create_still_configuration.assert_called_once()
        self.mock_picamera2.configure.assert_called_once()
        self.mock_picamera2.start.assert_called_once()
        self.assertFalse(handler.running)
        self.assertIsNone(handler.thread)
        self.assertEqual(handler.publisher, self.mock_publisher)

    def test_take_photo_success(self):
        def fake_switch_mode_and_capture_file(config, buffer, **kwargs):
            buffer.write(b'\xff\xd8\xff\xe0FakeJPEGData')
            buffer.seek(0)

        self.mock_picamera2.switch_mode_and_capture_file.side_effect = fake_switch_mode_and_capture_file
        handler = PiCameraHandler(self.mock_publisher)
        result = handler.take_photo()
        self.mock_picamera2.switch_mode_and_capture_file.assert_called_once()
        self.assertTrue(result.startswith(b'\xff\xd8\xff\xe0'))

    def test_cleanup_releases_camera(self):
        handler = PiCameraHandler(self.mock_publisher)
        handler.cleanup()
        self.mock_picamera2.close.assert_called_once()

    def test_stop_stops_thread(self):
        handler = PiCameraHandler(self.mock_publisher)
        handler.running = True
        handler.thread = threading.Thread(target=lambda: None)
        handler.thread.start()
        handler.stop()
        assert handler.running is False
        assert not handler.thread.is_alive()

    def test_start_sets_running_and_starts_thread(self):
        handler = PiCameraHandler(self.mock_publisher)
        handler.take_photo = MagicMock(return_value=b'fake_image_data')
        handler.start()
        assert handler.running is True
        assert handler.thread is not None
        assert isinstance(handler.thread, threading.Thread)
        time.sleep(0.1)
        assert handler.thread.is_alive()
        handler.stop()
        assert handler.running is False
