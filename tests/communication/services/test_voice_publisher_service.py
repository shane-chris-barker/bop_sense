from communication.services.voice_publisher_service import VoicePublisherService
from communication.publishers.mock_publisher import MockPublisher

def test_voice_publisher_service_publishes_correctly():
    mock_publisher = MockPublisher()
    service = VoicePublisherService(mock_publisher)
    command =  'Execute Order 66'
    service.send_to_publisher(command)

    assert len(mock_publisher.published_messages) == 1
    message = mock_publisher.published_messages[0]

    assert message.to_dict()["input"] == "mic"
    assert message.to_dict()["content"] == {'text': 'Execute Order 66'}
