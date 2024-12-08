from config import settings
from logger_config import logger
from utils.rabbitmq.manager import RabbitMQManager
from utils.rabbitmq.process_message import ProcessMessage


class RabbitMQConsumer:
    def __init__(self, manager: RabbitMQManager, callback: ProcessMessage):
        self.rabbitmq = manager
        self.process = callback

    async def consume_messages(self, queue_name):
        logger.info(f"Consuming on queue: {queue_name}")
        try:
            if not self.rabbitmq.connection or self.rabbitmq.connection.is_closed:
                await self.rabbitmq.connect()

            await self.rabbitmq.declare_exchange(exchange_name=settings.exchange)
            await self.rabbitmq.declare_queue(queue_name)
            await self.rabbitmq.bind_queue_to_exchange(routing_key=settings.routing_key)
            await self.rabbitmq.consume_queue(callback=self.process.process_message, no_ack=False)
            logger.info("Waiting for messages...")


        except Exception as e:
            logger.error(f"Error in consumer: {e}")
            raise
