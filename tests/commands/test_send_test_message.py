from unittest.mock import patch, MagicMock
from commands.send_test_message import send_test_message
from bop_common.enums.hardware_type import HardwareType
from bop_common.dtos.communication_dto import CommunicationDTO

def test_send_test_publishes_correctly():
    with patch("commands.send_test_message.get_publisher") as mock_get_publisher:
        mock_publisher = MagicMock()
        mock_get_publisher.return_value = mock_publisher
        send_test_message()
        mock_get_publisher.assert_called_once()
        mock_publisher.publish.assert_called_once()

        published_dto = mock_publisher.publish.call_args[0][0]
        assert isinstance(published_dto, CommunicationDTO)
        assert published_dto.input == HardwareType.TEST_HARDWARE
        assert published_dto.content == {"text":"Hello from bop sense"}