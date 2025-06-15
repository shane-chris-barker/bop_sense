import os
import logging

def setup_logging():
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    formatter_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    formatter = logging.Formatter(
        formatter_string
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logging.basicConfig(
        level=getattr(logging, log_level),
        handlers=[console_handler],
        format=formatter_string
    )
setup_logging()