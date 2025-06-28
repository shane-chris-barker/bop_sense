import pytest
from unittest.mock import patch
import os
from hardware_detection.services.hardware_config_service import HardwareConfigService
from bop_common.enums.hardware_type import HardwareType

class TestHardwareConfigService:
    mic_installed_key = "MIC_INSTALLED"
    usb_cam_installed_key = "USB_CAM_INSTALLED"
    pi_cam_installed_key = "PI_CAM_INSTALLED"

    @pytest.fixture(autouse=True)
    def clear_env(self, monkeypatch):
        monkeypatch.delenv(self.mic_installed_key, raising=False)
        monkeypatch.delenv(self.usb_cam_installed_key, raising=False)
        monkeypatch.delenv(self.pi_cam_installed_key, raising=False)

    def test_default_env_vars_disabled(self):
        service = HardwareConfigService()
        assert not service.is_device_enabled_in_config(HardwareType.MIC)
        assert not service.is_device_enabled_in_config(HardwareType.CAMERA)
        assert service.get_config_enabled_devices() == set()

    @pytest.mark.parametrize("mic_value", ["true", "1", "yes", "on","TRUE"])
    def test_enabled_var(self, mic_value, monkeypatch):
        monkeypatch.setenv(self.mic_installed_key, mic_value)
        service = HardwareConfigService()
        assert service.is_device_enabled_in_config(HardwareType.MIC)
        assert HardwareType.MIC in service.get_config_enabled_devices()

    @pytest.mark.parametrize("usb_cam_value, picam_value", [
        ("false", "false"),
        ("0", "false"),
        ("no", "false"),
        ("off", "false"),
        ("FALSE", "false"),
    ])
    def test_disabled_var(self, usb_cam_value, picam_value):
        test_env = {
            "USB_CAM_INSTALLED": usb_cam_value,
            "PI_CAM_INSTALLED": picam_value
        }
        with patch.dict(os.environ, test_env, clear=False):
            service = HardwareConfigService()
            assert not service.is_device_enabled_in_config(HardwareType.CAMERA)
            assert HardwareType.CAMERA not in service.get_config_enabled_devices()
