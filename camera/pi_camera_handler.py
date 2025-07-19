import base64
import time
try:
    from picamera2 import Picamera2
except ImportError:
    Picamera2 = None
import threading
import logging
import io

from camera.camera_handler_interface import CameraHandlerInterface
from communication.services.publisher_service_interface import PublisherServiceInterface
logger = logging.getLogger(__name__)

class PiCameraHandler(CameraHandlerInterface):
    def __init__(self, camera_publisher: PublisherServiceInterface):
        self.log_prefix = f"[📷 {self.__class__.__name__}]"
        self.publisher = camera_publisher
        self.running = False
        self.thread = None
        self.picam = Picamera2()

        config = self.picam.create_still_configuration(main={'format': 'RGB888', 'size':(320, 240)})
        self.picam.configure(config)
        self.picam.start()

    def start(self) -> None:
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._stream_loop, daemon=True)
        self.thread.start()

    def stop(self) -> None:
        if not self.running:
            return
        self.running = False
        if self.thread:
            self.thread.join()

    def cleanup(self) -> None:
        self.stop()
        if self.picam:
            self.picam.close()

    def take_photo(self) -> bytes:
        buffer = io.BytesIO()
        jpeg_config = self.picam.create_still_configuration(main={'format': 'RGB888', "size": (320, 240)})
        self.picam.switch_mode_and_capture_file(jpeg_config, buffer, format='jpeg', quality=50)
        buffer.seek(0)
        return buffer.getvalue()

    def _stream_loop(self) -> None:
        while self.running:
            try:
                image_bytes = self.take_photo()
                image_base64 = base64.b64encode(image_bytes).decode("utf-8")
                self.publisher.send_to_publisher(image_base64)
                logger.debug(f"{self.log_prefix} Captured a frame.")
            except Exception as e:
                logger.warning(f"{self.log_prefix} Error capturing or publishing image: {e}")
            time.sleep(5)
