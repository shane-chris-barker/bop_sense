import pytest
from unittest.mock import patch, MagicMock
from communication.publishers.amqp_publisher import AmqpPublisher
from communication.publishers.mqtt_publisher import MqttPublisher
from communication.publishers.mock_publisher import MockPublisher
from communication.factories.publisher_factory import get_publisher

patch_config = "communication.factories.publisher_factory.get_config"

@patch(patch_config)
@patch("communication.factories.publisher_factory.MqttPublisher")
def test_it_returns_mqtt_publisher(mock_mqtt_publisher_class, mock_get_config):
    mock_get_config.return_value = MagicMock(
        COMM_TYPE='mqtt',
        MQTT_HOST='localhost',
        MQTT_PORT=1883,
        COMM_NAME='test_topic'
    )

    mock_instance = MagicMock(spec=MqttPublisher)
    mock_mqtt_publisher_class.return_value = mock_instance
    publisher = get_publisher()
    mock_mqtt_publisher_class.assert_called_once_with(
        host='localhost',
        port=1883,
        topic='test_topic'
    )
    assert isinstance(publisher, MqttPublisher)

@patch(patch_config)
@patch("communication.factories.publisher_factory.AmqpPublisher")
def test_it_returns_amqp_publisher(mock_amqp_publisher_class, mock_get_config):
    mock_get_config.return_value = MagicMock(
        COMM_TYPE='amqp',
        AMQP_HOST='localhost',
        AMQP_PORT=5672,
        COMM_NAME='test_queue'
    )

    mock_instance = MagicMock(spec=AmqpPublisher)
    mock_amqp_publisher_class.return_value = mock_instance
    publisher = get_publisher()
    mock_amqp_publisher_class.assert_called_once_with(
        host='localhost',
        port=5672,
        queue_name='test_queue'
    )
    
    assert isinstance(publisher, AmqpPublisher)

@patch(patch_config)
@patch("communication.factories.publisher_factory.MqttPublisher")
def test_it_returns_mock_as_fallback(mock_mqtt_publisher_class, mock_get_config):
    mock_get_config.return_value = MagicMock(
        COMM_TYPE='mqtt',
        MQTT_HOST='localhost',
        MQTT_PORT=1883,
        COMM_NAME='test_topic'
    )

    mock_mqtt_publisher_class.side_effect = Exception("Connection failed")
    publisher = get_publisher()
    assert isinstance(publisher, MockPublisher)

@patch(patch_config)
def test_it_returns_mock_when_unsupported_publisher_type(mock_get_config):
    mock_get_config.return_value = MagicMock(
        COMM_TYPE='unsupported',
        MQTT_HOST='localhost',
        MQTT_PORT=1883,
        COMM_NAME='test_topic'
    )
    
    publisher = get_publisher()
    assert isinstance(publisher, MockPublisher)