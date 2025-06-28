from unittest.mock import MagicMock, patch
from hardware_detection.services.camera_service_starter import CameraServiceStarter
from hardware_detection.dtos.service_info_dto import ServiceInfoDTO
from hardware_detection.enums.service_name import ServiceType
from hardware_detection.enums.camera_type import CameraType
class TestCameraServiceStarter:
    @patch("hardware_detection.services.camera_service_starter.HardwareConfigService.get_enabled_camera_type",
           return_value=CameraType.USB)
    @patch("hardware_detection.services.camera_service_starter.get_publisher")
    @patch("hardware_detection.services.camera_service_starter.ImagePublisherService")
    @patch("hardware_detection.services.camera_service_starter.USBCameraHandler")
    @patch("hardware_detection.services.camera_service_starter.PiCameraHandler")
    def test_start_creates_and_returns_expected_service_info(
            self, mock_pi_cam_cls, mock_usb_cam_cls, mock_img_pub_cls, mock_get_pub, mock_get_cam_type
    ):
        mock_publisher = MagicMock()
        mock_get_pub.return_value = mock_publisher

        mock_usb_handler = MagicMock()
        mock_usb_cam_cls.return_value = mock_usb_handler

        mock_pi_handler = MagicMock()
        mock_pi_cam_cls.return_value = mock_pi_handler

        mock_img_publisher = MagicMock()
        mock_img_pub_cls.return_value = mock_img_publisher

        starter = CameraServiceStarter()
        result = starter.start()

        mock_get_pub.assert_called_once()
        mock_img_pub_cls.assert_called_once_with(mock_publisher)
        mock_usb_cam_cls.assert_called_once_with(mock_img_publisher)
        mock_usb_handler.start.assert_called_once()

        assert isinstance(result, ServiceInfoDTO)
        assert result.service == ServiceType.CAMERA
        assert result.instance == mock_usb_handler
