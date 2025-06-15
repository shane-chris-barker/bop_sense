import speech_recognition as sr
import threading
import logging
from communication.services.publisher_service_interface import PublisherServiceInterface

logger = logging.getLogger(__name__)
class VoiceListener:
    def __init__(self, voice_service: PublisherServiceInterface):
        self.voice_service = voice_service
        self.running = False
        self.listener_thread = None
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.log_prefix = f"[💬 {self.__class__.__name__}]"
    
    def start(self):
        if not self.running:
            self.running = True
            self.listener_thread = threading.Thread(target=self._continuous_listen, daemon=True)
            self.listener_thread.start()
    
    def stop(self):
        self.running = False
        if self.listener_thread and self.listener_thread.is_alive():
            self.listener_thread.join(timeout=1.0)

    def listen_for_command(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            logger.info(f"{self.log_prefix} Bop is listening..")
            audio = self.recognizer.listen(source)
        try:
            command = self.recognizer.recognize_google(audio).lower()
            logger.info(f"{self.log_prefix} Bop thinks you said:{command}")
            self.voice_service.send_to_publisher(command)
        except sr.UnknownValueError:
            logger.debug(f"{self.log_prefix} Bop's not sure what you said..")
        except sr.RequestError as e:
            logger.debug(f"{self.log_prefix} API error@ {e}")

    def _continuous_listen(self):
        while self.running:
            self.listen_for_command()
