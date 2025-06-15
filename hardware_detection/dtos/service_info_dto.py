from dataclasses import dataclass
from typing import Any, Optional
from hardware_detection.enums.service_name import ServiceType

@dataclass
class ServiceInfoDTO:
    service: ServiceType
    instance: Any
    cleanup_resource: Optional[Any] = None