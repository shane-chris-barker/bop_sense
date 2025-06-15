import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def load_env():
    env = os.getenv("BOP_ENV", "dev").lower()
    env_file = f".env.{env}"
    logging.info(f"loading env: {env} from {env_file}")
    load_dotenv(env_file)
    logger.debug(f"COMM_TYPE after load: {os.getenv('COMM_TYPE')}")

load_env()

class Config:
    COMM_TYPE = os.getenv("COMM_TYPE", "mock").lower()
    MQTT_HOST = os.getenv("MQTT_HOST")
    MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
    AMQP_HOST = os.getenv("AMQP_HOST")
    AMQP_PORT = int(os.getenv("AMQP_PORT", 5672))
    AMQP_QUEUE = os.getenv("AMQP_QUEUE")
    COMM_NAME = os.getenv("COMM_NAME")

def get_config() -> Config:
    return Config()