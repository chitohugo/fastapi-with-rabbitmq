from abc import ABC, abstractmethod


class NotificationServiceAbstract(ABC):
    @abstractmethod
    def send_notification(self, **kwargs) -> None:
        ...