from unittest.mock import patch, MagicMock
from bop_common.enums.hardware_type import HardwareType
from bop_common.enums.service_name import ServiceType
from bop_common.dtos.service_info_dto import ServiceInfoDTO
from hardware_detection.helpers.services_startup_helper import start_enabled_services

class TestServicesStartupHelper:
    patch_hardware_config = "hardware_detection.helpers.services_startup_helper.HardwareConfigService"
    patch_starters = "hardware_detection.helpers.services_startup_helper.SERVICE_STARTERS"

    @patch(patch_hardware_config)
    @patch(patch_starters)
    def test_returns_list_of_started_services(self, mock_registry, mock_config_service_cls):
        mock_service_instance = MagicMock()
        mock_service_info = ServiceInfoDTO(
            service=ServiceType.VOICE,
            instance=mock_service_instance,
            cleanup_resource=MagicMock()
        )

        mock_starter = MagicMock()
        mock_starter.start.return_value = mock_service_info
        mock_registry.get.return_value = mock_starter

        mock_config_service = MagicMock()
        mock_config_service.get_config_enabled_devices.return_value = {HardwareType.MIC}
        mock_config_service_cls.return_value = mock_config_service

        services = start_enabled_services()
        assert len(services) == 1
        assert services[0] == mock_service_info
        mock_starter.start.assert_called_once() 
    
    @patch(patch_hardware_config)
    @patch(patch_starters)
    def test_handles_start_failure_gracefully(self, mock_registry, mock_config_cls):
        mock_starter = MagicMock()
        mock_starter.start.side_effect = Exception("Oh Dear..")
        mock_registry.get.return_value = mock_starter

        mock_config_service = MagicMock()
        mock_config_service.get_config_enabled_devices.return_value = {HardwareType.MIC}
        mock_config_cls.return_value = mock_config_service

        services = start_enabled_services()

        assert services == []
        mock_starter.start.assert_called_once()

