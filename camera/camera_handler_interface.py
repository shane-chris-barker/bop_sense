from abc import ABC, abstractmethod

class CameraHandlerInterface(ABC):
    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def cleanup(self) -> None:
        pass

    @abstractmethod
    def take_photo(self) -> bytes:
        pass
