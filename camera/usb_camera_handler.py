import logging
import base64
import cv2
import threading
import time
from camera.camera_handler_interface import CameraHandlerInterface
from communication.services.publisher_service_interface import PublisherServiceInterface
logger = logging.getLogger(__name__)

class USBCameraHandler(CameraHandlerInterface):
    def __init__(self, image_publisher_service: PublisherServiceInterface):
        self.image_publisher_service = image_publisher_service
        self.running = False
        self.thread = None
        self.cap = cv2.VideoCapture(0)
        self.log_prefix = f"[📷 {self.__class__.__name__}]"

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._stream_loop, daemon=True)
        self.thread.start()

    def stop(self):
        if not self.running:
            return
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1)

    def cleanup(self):
        self.cap.release()

    def take_photo(self):
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to capture frame from USB camera.")
        resized_frame = cv2.resize(frame, (320, 240))
        success, encoded_image = cv2.imencode('.jpg', resized_frame,  [cv2.IMWRITE_JPEG_QUALITY, 50])
        if not success:
            raise RuntimeError("Failed to encode frame from USB camera.")
        return encoded_image.tobytes()

    def _stream_loop(self):
        while self.running:
            try:
                image_bytes = self.take_photo()
                image_base64 = base64.b64encode(image_bytes).decode("utf-8")
                logger.info(f"{self.log_prefix} Captured a frame.")
                self.image_publisher_service.send_to_publisher(image_base64)
            except Exception as e:
                logger.warning(f"{self.log_prefix} Error capturing or publishing image: {e}")
            time.sleep(5)
