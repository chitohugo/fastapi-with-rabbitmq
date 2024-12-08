
from abc import ABC, abstractmethod
from email.message import EmailMessage
from typing import Optional, List


class NotificationServiceAbstract(ABC):
    @abstractmethod
    def send_notification(self, **kwargs) -> None:
        ...