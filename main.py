import time
import logging
from logger_config import setup_logging
from hardware_detection.helpers.services_startup_helper import start_enabled_services
from hardware_detection.services.service_registry import SERVICE_STARTERS
from hardware_detection.services.hardware_config_service import HardwareConfigService
from hardware_detection.dtos.service_info_dto import ServiceInfoDTO
setup_logging()
logger = logging.getLogger(__name__)

def main():
    log_prefix = "[🤖 MAIN]"
    logger.info(f"{log_prefix} Bop sense is waking up and checking the configuration")
    services = start_enabled_services()
    if not services:
        logger.info(f"{log_prefix} Bop sense started no services and will not be communicate!")

    try:
        while True:
           time.sleep(0.1)
    except KeyboardInterrupt:
        logger.info(f"{log_prefix} Bop Sense Is Shutting down")
        for service in services:
            if service.cleanup:
                service.cleanup()

if __name__ == "__main__":
    main()