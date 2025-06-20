from bop_common.enums.hardware_type import HardwareType
from hardware_detection.services.service_registry import SERVICE_STARTERS
from hardware_detection.services.mic_service_starter import MicServiceStarter

def test_mic_service_is_registered():
    assert HardwareType.MIC in SERVICE_STARTERS
    assert isinstance(SERVICE_STARTERS[HardwareType.MIC], MicServiceStarter)

def test_registry_only_contains_known_hardware_types():
    valid_keys = {HardwareType.MIC, HardwareType.CAMERA}  # extend as needed
    for key in SERVICE_STARTERS:
        assert key in valid_keys, f"Unexpected key in registry: {key}"