import pytest
from unittest.mock import MagicMock, patch
from camera.usb_camera_handler import USBCameraHandler
import threading
import time
import numpy as np
import cv2

class TestUSBCameraHandler:
    @pytest.fixture
    def mock_image_service(self):
        return MagicMock()

    @pytest.fixture(autouse=True)
    def setup(self, mock_image_service):
        self.mock_cap = MagicMock()
        with patch("camera.usb_camera_handler.cv2.VideoCapture", return_value=self.mock_cap):
            self.image_service = mock_image_service
            self.handler = USBCameraHandler(self.image_service)

    def test_initialize(self, mock_image_service):
        assert self.handler.image_publisher_service is self.image_service
        assert self.handler.cap is self.mock_cap
        assert self.handler.running is False
        assert self.handler.thread is None
        assert "[📷 USBCameraHandler]" in self.handler.log_prefix

    def test_start_sets_running_and_starts_thread(self):
        self.handler.take_photo = MagicMock(return_value=b'fake_image_data')
        self.handler.start()
        assert self.handler.running is True
        assert self.handler.thread is not None
        assert isinstance(self.handler.thread, threading.Thread)
        time.sleep(0.1)
        assert self.handler.thread.is_alive()
        self.handler.stop()
        assert self.handler.running is False

    def test_stop_stops_thread(self):
        self.handler.running = True
        self.handler.thread = threading.Thread(target=lambda: None)
        self.handler.thread.start()
        self.handler.stop()
        assert self.handler.running is False
        assert not self.handler.thread.is_alive()

    def test_take_photo_success(self):
        mock_cap = MagicMock()
        fake_frame = np.ones((480, 640, 3), dtype=np.uint8)
        mock_cap.read = MagicMock(return_value=(True, fake_frame))
        self.handler.cap = mock_cap
        fake_encode = MagicMock()
        fake_encode.tobytes.return_value = b'fake_jpeg_bytes'
        with patch('cv2.resize') as mock_resize, patch('cv2.imencode') as mock_imencode:
            resized_frame = np.ones((240, 320, 3), dtype=np.uint8)
            mock_resize.return_value = resized_frame
            mock_imencode.return_value = (True, fake_encode)
            result = self.handler.take_photo()
            mock_cap.read.assert_called_once()
            mock_resize.assert_called_once_with(fake_frame, (320, 240))
            mock_imencode.assert_called_once_with('.jpg', resized_frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
            fake_encode.tobytes.assert_called_once()
            assert result == b'fake_jpeg_bytes'

    def test_take_photo_camera_read_failure(self):
        mock_cap = MagicMock()
        mock_cap.read = MagicMock(return_value=(False, None))
        self.handler.cap = mock_cap
        with pytest.raises(RuntimeError, match="Failed to capture frame from USB camera"):
            self.handler.take_photo()
        mock_cap.read.assert_called_once()

    def test_take_photo_encoding_failure(self):
        mock_cap = MagicMock()
        fake_frame = np.ones((480, 640, 3), dtype=np.uint8)  # Simulate a real camera frame
        mock_cap.read.return_value = (True, fake_frame)
        self.handler.cap = mock_cap

        with patch('cv2.resize') as mock_resize, patch('cv2.imencode') as mock_imencode:
            resized_frame = np.ones((240, 320, 3), dtype=np.uint8)
            mock_resize.return_value = resized_frame
            mock_imencode.return_value = (False, None)
            with pytest.raises(RuntimeError, match="Failed to encode frame from USB camera"):
                self.handler.take_photo()
            mock_cap.read.assert_called_once()
            mock_imencode.assert_called_once_with('.jpg', resized_frame, [cv2.IMWRITE_JPEG_QUALITY, 50])

    def test_cleanup_releases_camera(self):
        mock_cap = MagicMock()
        self.handler.cap = mock_cap
        self.handler.cleanup()
        mock_cap.release.assert_called_once()
