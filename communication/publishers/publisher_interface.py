from abc import ABC, abstractmethod
from communication.dtos.communication_dto import CommunicationDTO

class PublisherInterface(ABC):
    @abstractmethod
    def publish(self, message: CommunicationDTO) -> None:
        pass