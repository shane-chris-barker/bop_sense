import pytest
import json
import paho.mqtt.client as mqtt
from unittest.mock import patch
from bop_common.exceptions.publisher_exceptions import (
    PublisherConnectionException,
    PublisherPublishException
)
from communication.publishers.mqtt_publisher import MqttPublisher
from bop_common.enums.hardware_type import HardwareType
from bop_common.dtos.communication_dto import CommunicationDTO

patch_string = "communication.publishers.mqtt_publisher.mqtt.Client" 

class TestMqttPublisher:
    @patch(patch_string)
    def test_connection_exception_on_init(self, mock_mqtt_client):
        mock_client_instance = mock_mqtt_client.return_value
        mock_client_instance.connect.side_effect = Exception('connection error')
        
        with pytest.raises(PublisherConnectionException) as exc_info:
            MqttPublisher(host='localhost', port=1883, topic='test_topic')
        
        # Be very explicit about what we expect
        exception_message = str(exc_info.value)        
        assert "Could not connect to MQTT broker =>" in exception_message
        assert "connection error" in exception_message

    @patch(patch_string)
    def test_successful_connection_starts_loop(self, mock_mqtt_client):
        mock_client_instance = mock_mqtt_client.return_value
        mock_client_instance.connect.return_value = mqtt.MQTT_ERR_SUCCESS
        publisher = MqttPublisher(host='custom', port=1234, topic='custom')

        mock_client_instance.connect.assert_called_once_with('custom', 1234)
        mock_client_instance.loop_start.assert_called_once()

        assert publisher.host == 'custom'
        assert publisher.port == 1234
        assert publisher.topic == 'custom' 

    @patch(patch_string)
    def test_publish_success_with_qos(self, mock_mqtt_client, caplog):
        mock_client_instance = mock_mqtt_client.return_value
        mock_client_instance.connect.return_value = mqtt.MQTT_ERR_SUCCESS
        mock_client_instance.publish.return_value = (mqtt.MQTT_ERR_SUCCESS, 1)
        publisher = MqttPublisher(host='localhost', port=1883, topic='test_topic')
        message = CommunicationDTO(input=HardwareType.MIC, content={"foo":"bar"})

        with caplog.at_level("INFO"):
            publisher.publish(message)

        expected_payload = json.dumps(message.to_dict())
        mock_client_instance.publish.assert_called_once_with(
            'test_topic',
            expected_payload,
            qos=1
        )
        assert f"Published : {expected_payload}" in caplog.text

    @patch(patch_string)
    def test_publish_fails_with_mqtt_error_code(self, mock_mqtt_client):
        mock_client_instance = mock_mqtt_client.return_value
        mock_client_instance.connect.return_value = mqtt.MQTT_ERR_SUCCESS
        mock_client_instance.publish.return_value = (mqtt.MQTT_ERR_NO_CONN, 1)

        publisher = MqttPublisher(host='localhost', port=1883, topic='test_topic')
        message = CommunicationDTO(input=HardwareType.MIC, content={"foo":"bar"})

        with pytest.raises(PublisherPublishException) as exception:
            publisher.publish(message)
        
        assert "Failed to publish message =>" in str(exception.value)
 
    @patch(patch_string)
    def test_publish_fails_with_exception(self, mock_mqtt_client):
        mock_client_instance = mock_mqtt_client.return_value
        mock_client_instance.connect.return_value = mqtt.MQTT_ERR_SUCCESS
        mock_client_instance.publish.side_effect = Exception("Network Timeout")
        publisher = MqttPublisher(host='localhost', port=1883, topic='test_topic')
        message = CommunicationDTO(input=HardwareType.MIC, content={"foo":"bar"})

        with pytest.raises(PublisherPublishException) as exception:
            publisher.publish(message)
        
        assert "Failed to publish message =>" in str(exception.value)
        assert "Network Timeout" in str(exception.value)
    
    @patch(patch_string)
    def test_multiple_publishes_use_same_client(self, mock_mqtt_client):
        mock_client_instance = mock_mqtt_client.return_value
        mock_client_instance.connect.return_value = mqtt.MQTT_ERR_SUCCESS
        mock_client_instance.publish.return_value = (mqtt.MQTT_ERR_SUCCESS, 1)

        publisher = MqttPublisher(host='localhost', port=1883, topic='test_topic')
        message1 = CommunicationDTO(input=HardwareType.MIC, content={"message":"one"})
        message2 = CommunicationDTO(input=HardwareType.MIC, content={"message":"two"})
        publisher.publish(message1)
        publisher.publish(message2)
        mock_mqtt_client.assert_called_once()
        assert mock_client_instance.publish.call_count == 2

        expected_calls = [
            (('test_topic', json.dumps(message1.to_dict())), {'qos': 1}),
            (('test_topic', json.dumps(message2.to_dict())), {'qos': 1})
        ]
        actual_calls = mock_client_instance.publish.call_args_list
        for i, (expected_call, actual_call) in enumerate(zip(expected_calls, actual_calls)):
            assert actual_call.args[:2] == expected_call[0][:2], f"Call {i+1} args mismatch"
            assert actual_call.kwargs == expected_call[1], f"Call {i+1} kwargs mismatch"

    @patch(patch_string)
    def test_is_connected_returns_client_status(self, mock_mqtt_client):
        mock_client_instance = mock_mqtt_client.return_value
        mock_client_instance.connect.return_value = mqtt.MQTT_ERR_SUCCESS
        mock_client_instance.is_connected.return_value = True

        publisher = MqttPublisher(host='localhost', port=1883, topic='test_topic')
        assert publisher.is_connected() is True
        mock_client_instance.is_connected.assert_called_once()
    
    @patch(patch_string)
    def test_close_method_stops_and_disconnects(self, mock_mqtt_client):
        mock_client_instance = mock_mqtt_client.return_value
        mock_client_instance.connect.return_value = mqtt.MQTT_ERR_SUCCESS
        publisher = MqttPublisher(host='localhost', port=1883, topic='test_topic')
        publisher.close()
        mock_client_instance.loop_stop.assert_called_once()
        mock_client_instance.disconnect.assert_called_once()
    
    @patch(patch_string)
    def test_default_params_are_used(self, mock_mqtt_client):
        mock_client_instance = mock_mqtt_client.return_value
        mock_client_instance.connect.return_value = mqtt.MQTT_ERR_SUCCESS
        publisher = MqttPublisher()

        assert publisher.port == 1883
        assert publisher.host == 'localhost'
        assert publisher.topic == 'communications'
        mock_client_instance.connect.assert_called_once_with('localhost', 1883)
    
    @patch(patch_string)
    def test_publish_with_different_message_types(self, mock_mqtt_client):
        mock_client_instance = mock_mqtt_client.return_value
        mock_client_instance.connect.return_value = mqtt.MQTT_ERR_SUCCESS
        mock_client_instance.publish.return_value = (mqtt.MQTT_ERR_SUCCESS, 1)
        publisher = MqttPublisher(host='localhost', port=1883, topic='test_topic')

        message_types = [
            CommunicationDTO(input=HardwareType.MIC, content={"audio":"Hello, world"}),
            CommunicationDTO(input=HardwareType.CAMERA, content={"camera":"Base64Image"}),
            CommunicationDTO(input=HardwareType.CAMERA, content={"data":{"temperature":"25 degrees"}})
        ]

        for message in message_types:
            publisher.publish(message)
            expected_payload = json.dumps(message.to_dict())
            last_call = mock_client_instance.publish.call_args
            assert last_call.args[1] == expected_payload
            assert last_call.kwargs['qos'] == 1