from dataclasses import dataclass
from bop_common.enums.hardware_type import HardwareType
@dataclass
class HardwareConfigDTO:
    device_type: HardwareType
    enabled: bool
    env_key: str