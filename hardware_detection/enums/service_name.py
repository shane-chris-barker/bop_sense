from enum import Enum, auto
from dataclasses import dataclass

@dataclass
class ServiceType(Enum):
    VOICE = auto()