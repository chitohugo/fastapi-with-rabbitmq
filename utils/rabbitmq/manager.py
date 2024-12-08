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
        except AMQPConnectionError as e:
            logger.error(f"RabbitMQ connection error: {e}")
            raise

    async def declare_exchange(self, exchange_name, exchange_type="direct"):
        logger.info(f"Declaring exchange: {exchange_name}")
        try:
            self.exchange = await self.channel.declare_exchange(
                exchange_name,
                type=ExchangeType[exchange_type.upper()].value,
                durable=True
            )
        except aio_pika.exceptions.AMQPError as e:
            logger.error(f"Error declaring exchange: {e}")
            raise

    async def declare_queue(self, queue_name) -> Queue:
        logger.info(f"Declaring queue: {queue_name}")
        try:
            self.queue = await self.channel.declare_queue(queue_name, durable=True)
        except aio_pika.exceptions.AMQPError as e:
            logger.error(f"Error declaring queue: {e}")
            raise

    async def bind_queue_to_exchange(self, routing_key=None):
        logger.info(f"Binding queue to exchange with routing_key: {routing_key}")
        try:
            if not self.exchange or not self.queue:
                raise RuntimeError("Exchange and queue must be declared before binding")
            await self.queue.bind(exchange=self.exchange, routing_key=routing_key)
        except asyncio.TimeoutError as e:
            logger.error(f"Timeout while binding queue: {e}")
            raise

    async def basic_publish(self, routing_key, message):
        try:
            logger.info(f"Publishing message to exchange with routing_key: {routing_key}")
            await self.exchange.publish(
                Message(
                    body=json.dumps(message).encode(),
                    delivery_mode=DeliveryMode.PERSISTENT
                ),
                routing_key=routing_key
            )
        except aio_pika.exceptions.AMQPError as e:
            logger.error(f"Error publishing message: {e}")
            raise

    async def consume_queue(self, callback, no_ack=True):
        logger.info("Starting queue consumption")
        try:
            await self.queue.consume(callback, no_ack=no_ack)
        except Exception as e:
            logger.error(f"Error consuming queue: {e}")
            raise

    async def close(self):
        try:
            if self.channel:
                await self.channel.close()
            if self.connection:
                await self.connection.close()
        except Exception as e:
            logger.error(f"Error closing RabbitMQ connection: {e}")
