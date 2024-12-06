import json

from aio_pika.abc import AbstractIncomingMessage

from use_cases.utils.upload_file import FileProcessor
from logger_config import logger


class ProcessMessage:
    def __init__(self, upload_file: FileProcessor):
        self.upload_file = upload_file


    async def process_message(self, message: AbstractIncomingMessage):
        logger.info(f"Received: {message.body}")
        message = message.body.decode("utf-8")
        payload = json.loads(message)

        if payload["type"] == "upload_file":
            await self.upload_file.get_data(payload)

        if payload["type"] == "uploaded_file":
            logger.info(f"File uploaded: {payload}")


    async def process_file(self, payload: dict):
        await self.upload_file.get_data(payload)