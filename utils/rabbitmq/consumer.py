from config import settings
from logger_config import logger
from utils.rabbitmq.manager import RabbitMQManager
from utils.rabbitmq.process_message import ProcessMessage


class RabbitMQConsumer:
    def __init__(self, rabbitmq_manager: RabbitMQManager, callback: ProcessMessage):
        self.rabbitmq_manager = rabbitmq_manager
        self.process = callback

    async def consume_messages(self, queue_name):
        logger.info(f"Consuming on queue: {queue_name}")
        try:
            logger.info(f"Starting consuming on queue: {queue_name}")
            await self.rabbitmq_manager.declare_exchange(exchange_name=settings.exchange)
            await self.rabbitmq_manager.declare_queue(queue_name)
            await self.rabbitmq_manager.bind_queue_to_exchange(routing_key=queue_name)
            await self.rabbitmq_manager.consume_queue(
                self.process.process_message
            )
            logger.info(" [*] Waiting for messages. To exit press CTRL+C")

        except Exception as e:
            logger.error(e)
            raise
