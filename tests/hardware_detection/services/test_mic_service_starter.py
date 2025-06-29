from unittest.mock import patch, MagicMock
from hardware_detection.services.mic_service_starter import MicServiceStarter
from bop_common.enums.service_name import ServiceType
from bop_common.dtos.service_info_dto import ServiceInfoDTO

class TestMicServiceStarter:

    service_starter_patch = "hardware_detection.services.mic_service_starter"
    
    @patch(f"{service_starter_patch}.get_publisher")
    @patch(f"{service_starter_patch}.VoicePublisherService")
    @patch(f"{service_starter_patch}.VoiceListener")
    def test_start_creates_and_returns_expected_service_info(
        self, mock_voice_listener_cls, mock_voice_publisher_cls, mock_get_publisher
    ):
        mock_publisher = MagicMock()
        mock_get_publisher.return_value = mock_publisher

        mock_voice_publisher = MagicMock()
        mock_voice_publisher_cls.return_value = mock_voice_publisher
        
        mock_voice_listener = MagicMock()
        mock_voice_listener_cls.return_value = mock_voice_listener

        starter = MicServiceStarter()
        result: ServiceInfoDTO = starter.start()

        mock_get_publisher.assert_called_once()
        mock_voice_publisher_cls.assert_called_once_with(mock_publisher)
        mock_voice_listener_cls.assert_called_once_with(mock_voice_publisher)
        mock_voice_listener.start.assert_called_once()

        assert isinstance(result, ServiceInfoDTO)
        assert result.service == ServiceType.VOICE
        assert result.instance == mock_voice_listener
        assert result.cleanup_resource == mock_voice_publisher
