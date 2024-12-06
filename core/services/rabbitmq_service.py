from utils.rabbitmq.producer import RabbitMQProducer


class RabbitMQService:
    def __init__(self, producer: RabbitMQProducer):
        self.producer = producer

    async def publish(self, routing_key=None, message=None):
        return await self.producer.publish_message(routing_key, message)
