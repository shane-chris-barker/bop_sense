import pytest
from pika.exceptions import AMQPError
import json
import logging
from unittest.mock import patch, MagicMock
from hardware_detection.enums.hardware_type import HardwareType
from communication.publishers.amqp_publisher import AmqpPublisher
from communication.dtos.communication_dto import CommunicationDTO
from communication.exceptions.publisher_exceptions import (
    PublisherPublishException,
    PublisherConnectionException
)
patch_string = "communication.publishers.amqp_publisher.pika.BlockingConnection"

class TestAmqpPublisher:

    def test_connection_exception_on_init(self):
        with pytest.raises(PublisherConnectionException) as exception:
            AmqpPublisher()
        assert "Could not connect to AMQP broker" in str(exception.value)

    def test_publish_exception_when_basic_publish_fails(self):
        mock_channel = MagicMock()
        mock_channel.queue_declare = MagicMock()
        mock_channel.basic_publish = MagicMock(side_effect=AMQPError('publish failed'))

        mock_connection = MagicMock()
        mock_connection.is_closed = False
        mock_connection.channel.return_value = mock_channel

        with patch("communication.publishers.amqp_publisher.pika.BlockingConnection", return_value=mock_connection):
            publisher = AmqpPublisher(host='localhost', port=5672, queue_name='communications')

        dummy_message = MagicMock(spec=CommunicationDTO)
        dummy_message.to_dict.return_value = {'foo': 'bar'}

        with pytest.raises(PublisherPublishException) as exception:
            publisher.publish(dummy_message)

        assert "Failed to publish message" in str(exception.value)

    def test_publish_success(self, caplog):
        mock_channel = MagicMock()
        mock_channel.queue_declare.return_value = None
        mock_channel.basic_publish.return_value = None
        mock_connection = MagicMock()
        mock_connection.is_closed = False
        mock_connection.channel.return_value = mock_channel
        with patch(patch_string, return_value=mock_connection):
            publisher = AmqpPublisher()
            message = CommunicationDTO(input=HardwareType.MIC, content={"text":"hello"})
            with caplog.at_level(logging.INFO):
                publisher.publish(message)

        expected_body = json.dumps(message.to_dict())
        properties = mock_channel.basic_publish.call_args[1]['properties']

        mock_channel.basic_publish.assert_called_once_with(
            exchange='',
            routing_key='communications',
            body=expected_body,
            properties=properties
        )
        assert properties.delivery_mode == 2
        assert f"Published : {expected_body}" in caplog.text
    
    def test_queue_only_declared_once(self):
        mock_channel = MagicMock()
        mock_connection = MagicMock()
        mock_connection.is_closed = False
        mock_connection.channel.return_value = mock_channel

        with patch(patch_string, return_value=mock_connection):
            publisher = AmqpPublisher()
            message = CommunicationDTO(input=HardwareType.MIC, content={"foo":"bar"})

            publisher.publish(message)
            publisher.publish(message)

            mock_channel.queue_declare.assert_called_once_with(
                queue='communications',
                durable=True
            )

    def test_reconnection_on_closed_connection(self):
        mock_connection1 = MagicMock()
        mock_connection2 = MagicMock()
        mock_connection1.is_closed = True
        mock_connection2.is_closed = False

        mock_channel = MagicMock()
        mock_connection2.channel.return_value = mock_channel

        with patch(patch_string, side_effect=[mock_connection1, mock_connection2]):
            publisher = AmqpPublisher()
            message = CommunicationDTO(
                input=HardwareType.MIC,
                content={"foo":"bar"}
            )

            publisher.publish(message)
            assert publisher.connection == mock_connection2
    
    def test_close_connnection(self):
        mock_connection = MagicMock()
        mock_connection.is_closed = False

        with patch(patch_string, return_value=mock_connection):
            publisher = AmqpPublisher()
            publisher.close()
            mock_connection.close.assert_called_once()
    
    def test_close_when_no_connection(self):
        publisher = AmqpPublisher.__new__(AmqpPublisher)
        publisher.connection = None
        publisher.close()

    def test_close_when_connection_already_closed(self):
        mock_connection = MagicMock()
        mock_connection.is_closed = True
        publisher = AmqpPublisher.__new__(AmqpPublisher)
        publisher.connection = mock_connection
        publisher.close()
        mock_connection.close.assert_not_called()

    def test_custom_params_are_used(self):
        mock_connection = MagicMock()
        mock_connection.is_closed = False

        with patch(patch_string, return_value=mock_connection) as mock:
            with patch("communication.publishers.amqp_publisher.pika.ConnectionParameters") as mock_params:
                publisher = AmqpPublisher(
                    host='custom',
                    port=1234,
                    queue_name='custom'
                )
            
            mock_params.assert_called_once_with(host='custom', port=1234)
            assert publisher.queue_name == 'custom'