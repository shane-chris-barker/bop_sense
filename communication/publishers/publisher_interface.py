from abc import ABC, abstractmethod
from bop_common.dtos.communication_dto import CommunicationDTO

class PublisherInterface(ABC):
    @abstractmethod
    def publish(self, message: CommunicationDTO) -> None:
        pass