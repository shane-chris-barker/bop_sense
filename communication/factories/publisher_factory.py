import logging
from communication.publishers.amqp_publisher import AmqpPublisher
from communication.publishers.mock_publisher import MockPublisher
from communication.publishers.mqtt_publisher import MqttPublisher
from communication.publishers.publisher_interface import PublisherInterface
from config import get_config

logger = logging.getLogger(__name__)

def get_publisher() -> PublisherInterface:
    config = get_config()
    log_prefix = "[📢 PUBLISHER FACTORY]"
    logger.info(f"{log_prefix} is trying to start the {config.COMM_TYPE} Publisher...")
    try:
        if config.COMM_TYPE == 'mqtt':
            publisher = MqttPublisher(
                host=config.MQTT_HOST,
                port=config.MQTT_PORT,
                topic=config.COMM_NAME
            )
            logger.info(f"{log_prefix} 🦟 MQTT Publisher created successfully")
            return publisher
        elif config.COMM_TYPE == 'amqp':
            publisher = AmqpPublisher(
                host=config.AMQP_HOST,
                port=config.AMQP_PORT,
                queue_name=config.COMM_NAME
            )
            logger.info(f"{log_prefix} 🐇 AMQP Publisher created successfully")
            return publisher
        elif config.COMM_TYPE == 'mock':
            publisher = MockPublisher()
            logger.info(f"{log_prefix} 🥷 Mock Publisher created successfully")
            return publisher
        else:
            raise ValueError(f"{log_prefix} Unsupported Publisher Type")
    except Exception as e:
        logger.warning(f"{log_prefix} Warning: Cannot boot Publisher - Falling back to mock because of {e}")
        return MockPublisher()