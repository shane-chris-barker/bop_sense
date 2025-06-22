from bop_common.dtos.communication_dto import CommunicationDTO
from communication.factories.publisher_factory import get_publisher
from bop_common.enums.hardware_type import HardwareType

def send_test_message():
    print("Starting debug message command...")
   
    publisher = get_publisher()
    print(f"Publisher is: {publisher}")

    publisher.publish(
        CommunicationDTO(
            input=HardwareType.TEST_HARDWARE,
            content={"text":"Hello from bop sense"}
        )
    )
    print("Publish called")
if __name__ == "__main__":
    send_test_message()
