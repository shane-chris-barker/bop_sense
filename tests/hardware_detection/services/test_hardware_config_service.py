import pytest
from hardware_detection.services.hardware_config_service import HardwareConfigService
from hardware_detection.enums.hardware_type import HardwareType

class TestHardwareConfigService:
    mic_installed_key = "MIC_INSTALLED"
    cam_installed_key = "CAM_INSTALLED"

    @pytest.fixture(autouse=True)
    def clear_env(self, monkeypatch):
        monkeypatch.delenv(self.mic_installed_key, raising=False)
        monkeypatch.delenv(self.cam_installed_key, raising=False)
        
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

    @pytest.mark.parametrize("cam_value", ["false", "0", "no", "off","FALSE"])
    def test_disabled_var(self, cam_value, monkeypatch):
        monkeypatch.setenv(self.cam_installed_key, cam_value)
        service = HardwareConfigService()
        assert not service.is_device_enabled_in_config(HardwareType.CAMERA)
        assert HardwareType.CAMERA not in service.get_config_enabled_devices()
