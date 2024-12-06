import asyncio
import json

import aio_pika
from aio_pika.exceptions import AMQPConnectionError
from aio_pika import ExchangeType, connect, Queue, Message, DeliveryMode

from logger_config import logger


class RabbitMQManager:
    def __init__(self, url):
        self.url = url
        self.channel = None
        self.connection = None
        self.queue = None
        self.exchange = None

    async def connect(self):
        try:
            self.connection = await connect(self.url)
            self.channel = await self.connection.channel()
            logger.info("Successful connection to RabbitMQ.")
            return
        except AMQPConnectionError as e:
            logger.error(f"RabbitMQ connection error: {e}")
            raise

    async def declare_exchange(self, exchange_name, exchange_type="direct"):
        logger.info("Declaring exchange")
        try:
            self.exchange = await self.channel.declare_exchange(
                exchange_name,
                type=ExchangeType[exchange_type.upper()].value,
                durable=True
            )
            return self.exchange

        except aio_pika.exceptions.AMQPError as e:
            logger.error(e)
            raise

    async def declare_queue(self, queue_name) -> Queue:
        logger.info("Declaring queue")
        try:
            self.queue = await self.channel.declare_queue(
                queue_name,
                durable=True
            )
            return self.queue

        except aio_pika.exceptions.ChannelClosed as e:
            logger.error(e)
            raise

    async def bind_queue_to_exchange(self, routing_key=None) -> None:
        logger.info("Bind queue")
        try:
            await self.queue.bind(
                exchange=self.exchange,
                routing_key=routing_key
            )
        except asyncio.TimeoutError as e:
            logger.error(e)
            raise

    async def basic_publish(self, message, routing_key):
        try:
            await self.exchange.publish(
                Message(
                    body=json.dumps(message).encode(),
                    delivery_mode=DeliveryMode.PERSISTENT
                ),
                routing_key=routing_key
            )
            return True

        except aio_pika.exceptions.AMQPError as e:
            logger.error(e)
            raise

    async def consume_queue(self, callback) -> bool:
        logger.info("Start listening the queue")
        try:
            await self.queue.consume(
                callback,
                no_ack=True
            )
            return True

        except asyncio.TimeoutError as e:
            logger.error(e)

    async def close(self):
        try:
            await self.channel.close()
            await self.connection.close()
        except Exception as e:
            logger.error(f"Error occurred while closing AMQP connection: {e}")
