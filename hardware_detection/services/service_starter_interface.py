from abc import ABC, abstractmethod
from hardware_detection.dtos.service_info_dto import ServiceInfoDTO

class ServiceStarterInterface(ABC):

    @abstractmethod
    def start(self) -> ServiceInfoDTO:
        pass
