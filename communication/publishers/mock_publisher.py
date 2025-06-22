import logging
from communication.publishers.publisher_interface import PublisherInterface
from bop_common.dtos.communication_dto import CommunicationDTO

logger = logging.getLogger(__name__)

class MockPublisher(PublisherInterface):
    def __init__(self):
        self.published_messages = []
        self.log_prefix = f"[🥷 {self.__class__.__name__}]"

    def publish(self, message: CommunicationDTO) -> None:
        self.published_messages.append(message)
        logger.info(f"{self.log_prefix} Pretending to publish: {message}")
