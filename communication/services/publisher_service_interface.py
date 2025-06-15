from abc import ABC, abstractmethod

class PublisherServiceInterface(ABC):
    @abstractmethod
    def send_to_publisher(self, data: str) -> None:
        pass