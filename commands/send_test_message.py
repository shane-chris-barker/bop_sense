import logging

from communication.dtos.communication_dto import CommunicationDTO
from communication.factories.publisher_factory import get_publisher
from hardware_detection.enums.hardware_type import HardwareType

logger = logging.getLogger(__name__)

def send_test_message():
    logger.info("Starting debug message command...")
   
    publisher = get_publisher()
    logger.info(f"Publisher is: {publisher}")

    publisher.publish(
        CommunicationDTO(
            input=HardwareType.TEST_HARDWARE,
            content={"text":"Hello from bop sense"}
        )
    )
    logger.info("Publish called")
if __name__ == "__main__":
    send_test_message()