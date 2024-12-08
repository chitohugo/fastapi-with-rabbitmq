import json

from aio_pika.abc import AbstractIncomingMessage

from logger_config import logger
from utils.email_notification.send_email import EmailNotification


class ProcessMessage:
    def __init__(self, email_service: EmailNotification):
        self.service = email_service

    async def process_message(self, message: AbstractIncomingMessage):
        logger.info(f"Received message: {message.body}")
        try:
            payload = json.loads(message.body.decode("utf-8"))
            logger.info(f"Processing message: {payload}")
            data = {
                "recipient": payload["email"],
                "subject": "Character created",
                "message": f"Character {payload['name']} has been created"
            }
            await self.service.send_notification(**data)
            await message.ack()
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            await message.nack(requeue=False)

