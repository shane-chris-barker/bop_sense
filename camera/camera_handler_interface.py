from abc import ABC, abstractmethod

class CameraHandlerInterface(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def cleanup(self):
        pass

    @abstractmethod
    def take_photo(self):
        pass
