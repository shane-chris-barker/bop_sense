from logging import getLogger
from bop_common.dtos.communication_dto import CommunicationDTO
from bop_common.enums.hardware_type import HardwareType
from bop_common.exceptions.publisher_exceptions import PublisherPublishException
from communication.publishers.publisher_interface import PublisherInterface
from communication.services.publisher_service_interface import PublisherServiceInterface
logger = getLogger(__name__)

class ImagePublisherService(PublisherServiceInterface):
    def __init__(self, publisher: PublisherInterface):
        self.log_prefix = '[📷 Image Publisher]'
        self.publisher = publisher
        self.camera_type = None
    def send_to_publisher(self, data: str):
        dto = CommunicationDTO(input=HardwareType.CAMERA, content={'type':'image', 'data':data})
        try:
            self.publisher.publish(dto)
        except PublisherPublishException as e:
            logger.warning(f"{self.log_prefix} Communications not being published {e}")
