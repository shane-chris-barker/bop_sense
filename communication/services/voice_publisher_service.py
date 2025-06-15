import logging
from communication.dtos.communication_dto import CommunicationDTO
from communication.publishers.publisher_interface import PublisherInterface
from hardware_detection.enums.hardware_type import HardwareType
from communication.exceptions.publisher_exceptions import PublisherPublishException
from communication.services.publisher_service_interface import PublisherServiceInterface
logger = logging.getLogger(__name__)
class VoicePublisherService(PublisherServiceInterface):
    def __init__(self, publisher: PublisherInterface):
        self.publisher = publisher
    def send_to_publisher(self, data: str):
        dto = CommunicationDTO(input=HardwareType.MIC,  content={'text':data})
        try:
            self.publisher.publish(dto)
        except PublisherPublishException as e:
            logger.warning(f"[VOICE PUBLISHER] Communications not being published {e}")
