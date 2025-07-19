from datetime import datetime, timedelta
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
        self.stop_listening_at = None
        self.listen_word = 'listen'
    
    def start(self) -> None:
        if not self.running:
            self.running = True
            self.listener_thread = threading.Thread(target=self._continuous_listen, daemon=True)
            self.listener_thread.start()
    
    def stop(self) -> None:
        self.running = False
        if self.listener_thread and self.listener_thread.is_alive():
            self.listener_thread.join(timeout=1.0)

    def listen_for_command(self) -> None:
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            if not self._is_actively_listening():
                logger.info(f"{self.log_prefix} Bop is listening for the keyword {self.listen_word}")
            else:
                logger.info(f"{self.log_prefix} Bop is in the listening window")
            audio = self.recognizer.listen(source)
        try:
            command = self.recognizer.recognize_google(audio, language='en-GB').lower()
            if self._is_listen_command(command):
                logger.info(f"{self.log_prefix} Bop heard the keyword - Starting to listen.")
                self._activate_listening_window()
            elif self._is_actively_listening():
                logger.info(f"{self.log_prefix} Bop Listened and heard {command} - Publishing!")
                self.voice_service.send_to_publisher(command)
            else:
                logger.info(f"{self.log_prefix} Bop is ignoring command {command} - not in listening mode")

        except sr.UnknownValueError:
            logger.info(f"{self.log_prefix} Bop's not sure what you said..")
        except sr.RequestError as e:
            logger.info(f"{self.log_prefix} Bop fell over - API error@ {e}")

    def _continuous_listen(self) -> None:
        while self.running:
            self.listen_for_command()

    def _is_listen_command(self, command: str) -> bool:
        return self.listen_word in command

    def _is_actively_listening(self) -> bool:
        if self.stop_listening_at is None:
            return False
        is_active = datetime.now() < self.stop_listening_at
        if not is_active:
            self.stop_listening_at = None
        return is_active

    def _activate_listening_window(self) -> None:
        self.stop_listening_at = datetime.now() + timedelta(seconds=10)
