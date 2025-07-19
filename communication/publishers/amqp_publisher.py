import pika
import json
import logging 
import pika.adapters.blocking_connection
from pika.exceptions import AMQPError
from typing import Optional
from communication.publishers.publisher_interface import PublisherInterface
from bop_common.dtos.communication_dto import CommunicationDTO
from bop_common.exceptions.publisher_exceptions import (
    PublisherConnectionException, 
    PublisherPublishException
)

logger = logging.getLogger(__name__)

class AmqpPublisher(PublisherInterface):
    connection: Optional[pika.BlockingConnection]
    channel: Optional[pika.adapters.blocking_connection.BlockingChannel]
    failed_to_connect_error = "Could not connect to AMQP broker =>"
    failed_to_publish_message = "Failed to publish message =>"
    success_publish_message = "Published"
     
    def __init__(self, host='localhost', port=5672, queue_name='communications'):
        self.log_prefix =  f"[🐇 {self.__class__.__name__}]"
        logging.info(f"{self.log_prefix} Attempting to start AMQP Publisher")
        self.host = host
        self.port = port
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        self.queue_declared = False
        self._ensure_connection()

    def _ensure_connection(self) -> None:
        if self.connection is None or self.connection.is_closed:
            try:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port))
                self.channel = self.connection.channel()
            except AMQPError as e:
                raise PublisherConnectionException(f"{self.log_prefix} {self.failed_to_connect_error} {e}")

    def publish(self, message:CommunicationDTO) -> None:
        try:
            self._ensure_connection()
            if not self.queue_declared:
                self.channel.queue_declare(queue=self.queue_name, durable=True)
                self.queue_declared = True

            body = json.dumps(message.to_dict())
            body_bytes = body.encode('utf-8')
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=body_bytes,
                properties=pika.BasicProperties(delivery_mode=2)
            )
        except AMQPError as e:
            raise PublisherPublishException(f"{self.log_prefix} {self.failed_to_publish_message} {e}")
        logger.info(f"{self.log_prefix} {self.success_publish_message} : {body}")

    def close(self) -> None:
        if self.connection and not self.connection.is_closed:
            self.connection.close()
