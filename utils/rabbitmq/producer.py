from config import settings
from logger_config import logger
from utils.rabbitmq.manager import RabbitMQManager


class RabbitMQProducer:
    def __init__(self, rabbitmq_manager: RabbitMQManager):
        self.rabbitmq_manager = rabbitmq_manager

    async def publish_message(self, routing_key=None, message=None):
        """Method to publish message to RabbitMQ"""
        try:
            logger.info(f"Publishing message: {message}")
            if self.rabbitmq_manager.connection is None or self.rabbitmq_manager.connection.is_closed:
                await self.rabbitmq_manager.connect()

            if not self.rabbitmq_manager.exchange:
                await self.rabbitmq_manager.declare_exchange(
                    exchange_name=settings.exchange
                )

            await self.rabbitmq_manager.basic_publish(
                routing_key,
                message
            )
            logger.info("Message published successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            raise
