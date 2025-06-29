from camera.pi_camera_handler import PiCameraHandler
from hardware_detection.services.hardware_config_service import HardwareConfigService
from bop_common.interfaces.service_starter_interface import ServiceStarterInterface
from hardware_detection.enums.camera_type import CameraType
from bop_common.enums.service_name import ServiceType
from bop_common.dtos.service_info_dto import ServiceInfoDTO
from communication.services.image_publisher_service import ImagePublisherService
from communication.factories.publisher_factory import get_publisher
from camera.usb_camera_handler import USBCameraHandler

class CameraServiceStarter(ServiceStarterInterface):

    def __init__(self):
        self.config_service = HardwareConfigService()

    def start(self) -> ServiceInfoDTO:
        cam_type = self.config_service.get_enabled_camera_type()
        if cam_type == CameraType.USB:
            handler = USBCameraHandler(ImagePublisherService(get_publisher()))
        elif cam_type == CameraType.PI:
            handler = PiCameraHandler(ImagePublisherService(get_publisher()))
        else:
            raise RuntimeError("No camera enabled in config.")

        handler.start()
        return ServiceInfoDTO(service=ServiceType.CAMERA, instance=handler)
