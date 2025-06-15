class PublisherConnectionException(Exception):
    """Raised when the publisher cannot connect to the message broker."""

class PublisherPublishException(Exception):
    """Raised when publishing a message fails."""  