import pytest

from communication.exceptions.publisher_exceptions import (
    PublisherConnectionException,
    PublisherPublishException
)

connection_failed_exception = "connection failed"
publishing_failed_exception = 'publish failed'

def test_exceptions_can_be_instantiated_without_raising():
    assert str(PublisherConnectionException(connection_failed_exception)) == connection_failed_exception
    assert str(PublisherPublishException(publishing_failed_exception)) == publishing_failed_exception

def test_publisher_connection_exception_raises():
    with pytest.raises(PublisherConnectionException) as exception:
        raise PublisherConnectionException(connection_failed_exception)
    assert str(exception.value) == connection_failed_exception

def test_publisher_publish_exception_raises():
    with pytest.raises(PublisherPublishException) as exception:
        raise PublisherPublishException(publishing_failed_exception)
    assert str(exception.value) == publishing_failed_exception