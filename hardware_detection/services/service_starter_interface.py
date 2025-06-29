from abc import ABC, abstractmethod
from bop_common.dtos.service_info_dto import ServiceInfoDTO

class ServiceStarterInterface(ABC):

    @abstractmethod
    def start(self) -> ServiceInfoDTO:
        pass
