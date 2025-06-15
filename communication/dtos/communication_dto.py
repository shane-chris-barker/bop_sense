from dataclasses import dataclass
from typing import Dict, Any
from hardware_detection.enums.hardware_type import HardwareType

@dataclass
class CommunicationDTO:
    input: HardwareType
    content: Dict[str, Any]

    @staticmethod
    def from_dict(data: Dict) -> 'CommunicationDTO':
        return CommunicationDTO(
            input=HardwareType(data["input"]),
            content=data["content"]
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "input": self.input.value,
            "content": self.content
        }
