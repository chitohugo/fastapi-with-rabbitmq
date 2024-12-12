from abc import ABC, abstractmethod


class EmailServiceAbstract(ABC):
    @abstractmethod
    def send_email(self, recipient: str, subject: str, rendered_html: str, is_html: bool = False):
        ...