import os
from typing import Set
import logging
from bop_common.enums.hardware_type import HardwareType
from bop_common.dtos.hardware_config_dto import HardwareConfigDTO
from hardware_detection.enums.camera_type import CameraType
logger = logging.getLogger(__name__)

class HardwareConfigService:
    mic_activated_env_key = "MIC_INSTALLED"
    usb_cam_activated_env_key = "USB_CAM_INSTALLED"
    pi_cam_activated_env_key = "PI_CAM_INSTALLED"
    status_service_enabled_string = "ENABLED"
    status_service_disabled_string = "DISABLED"

    def __init__(self):
        self.log_prefix =  f"[🔧 {self.__class__.__name__}]"
        self._device_configs = {
            HardwareType.MIC: HardwareConfigDTO(
                device_type=HardwareType.MIC,
                enabled=self._get_env_bool(self.mic_activated_env_key, False),
                env_key=self.mic_activated_env_key
            ),
            HardwareType.CAMERA: HardwareConfigDTO(
                device_type=HardwareType.CAMERA,
                enabled=(
                        self._get_env_bool(self.usb_cam_activated_env_key, False) or
                        self._get_env_bool(self.pi_cam_activated_env_key, False)
                ),
                env_key=""
            ),
        }
        self._log_configuration()

    @staticmethod
    def _get_env_bool(key: str, default: bool = False) -> bool:
        env_value = os.getenv(key)
        print(f"[DEBUG] Reading env var '{key}' = {env_value}")

        if env_value is None:
            return default
        return env_value.lower() in ('true', '1', 'yes', 'on')
    
    def _log_configuration(self) -> None:
        logger.info(f"{self.log_prefix} Device Configuration:")
        for device_type, config in self._device_configs.items():
            status = self.status_service_enabled_string if config.enabled else self.status_service_disabled_string
            logger.info(f"{self.log_prefix} {device_type.value.upper()} IS {status}")

    def is_device_enabled_in_config(self, device_type: HardwareType) -> bool:
        config = self._device_configs.get(device_type)
        return config.enabled if config else False
    
    def get_config_enabled_devices(self) -> Set[HardwareType]:
        return {
            device_type for device_type, config in self._device_configs.items()
            if config.enabled
        }

    def get_enabled_camera_type(self) -> CameraType | None:
        if self._get_env_bool(self.usb_cam_activated_env_key):
            return CameraType.USB
        elif self._get_env_bool(self.pi_cam_activated_env_key):
            return CameraType.PI
        return None