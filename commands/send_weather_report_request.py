from bop_common.dtos.communication_dto import CommunicationDTO
from communication.factories.publisher_factory import get_publisher
from bop_common.enums.hardware_type import HardwareType

def send_request_weather_report():
    print("Starting to request weather report")

    publisher = get_publisher()
    print(f"Publisher is: {publisher}")

    publisher.publish(
        CommunicationDTO(
            input=HardwareType.MIC,
            content={"text": "weather forecast"}
        )
    )
    print("Publish called")
if __name__ == "__main__":
    send_request_weather_report()
