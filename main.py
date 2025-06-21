import logging
from logger_config import setup_logging
setup_logging()
import time
from hardware_detection.helpers.services_startup_helper import start_enabled_services
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
            if hasattr(service.instance, 'cleanup') and callable(service.instance.cleanup):
                service.instance.cleanup()

if __name__ == "__main__":
    main()