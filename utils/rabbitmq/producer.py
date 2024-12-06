from config import settings
from logger_config import logger
from utils.rabbitmq.manager import RabbitMQManager


class RabbitMQProducer:
    def __init__(self, rabbitmq_manager: RabbitMQManager):
        self.rabbitmq_manager = rabbitmq_manager

    async def publish_message(self, routing_key, message):
        """Method to publish message to RabbitMQ
        Args
            routing_key (str): routing key
            message (str): to be published
        Returns
            Boolean: True if message was published successfully
            Raises an exception if message could not be published
        """
        try:
            logger.info(f"Publishing message: {message}")
            if self.rabbitmq_manager.connection is None or self.rabbitmq_manager.connection.is_closed:
                await self.rabbitmq_manager.connect()

            await self.rabbitmq_manager.declare_exchange(exchange_name=settings.exchange)
            await self.rabbitmq_manager.basic_publish(message, routing_key)
            logger.info("Message published")

        except Exception as e:
            logger.error(e)
            raise

        return True
