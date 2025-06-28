from communication.services.image_publisher_service import ImagePublisherService
from communication.publishers.mock_publisher import MockPublisher
from bop_common.enums.hardware_type import HardwareType

def test_image_publisher_service_publishes_correctly():
    mock_publisher = MockPublisher()
    service = ImagePublisherService(mock_publisher)
    image_data = 'IM_A_BASE_64_IMAGE!'
    service.send_to_publisher(image_data)

    assert len(mock_publisher.published_messages) == 1
    message = mock_publisher.published_messages[0]
    assert message.to_dict()['input'] == HardwareType.CAMERA.value
    assert message.to_dict()['content'] == {'type': 'image', 'data': image_data}
