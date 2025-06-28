from bop_common.enums.hardware_type import HardwareType
from hardware_detection.services.camera_service_starter import CameraServiceStarter
from hardware_detection.services.mic_service_starter import MicServiceStarter
from hardware_detection.services.service_starter_interface import ServiceStarterInterface

SERVICE_STARTERS: dict[HardwareType, ServiceStarterInterface] = {
    HardwareType.MIC: MicServiceStarter(),
    HardwareType.CAMERA: CameraServiceStarter()
}
