import smtplib
from email.message import EmailMessage

from utils.email_notification.abstract_notification import NotificationServiceAbstract
from utils.email_notification.smtp_service import SMTPService


class EmailNotification(NotificationServiceAbstract):
    def __init__(self, smtp_service: SMTPService):
        self.smtp_service = smtp_service

    async def send_notification(
        self,
        recipient: str,
        subject: str,
        message: str
    ) -> None:
        if not self._validate_email(recipient):
            raise ValueError("The email recipient is invalid.")

        email = EmailMessage()
        email["From"] = self.smtp_service.username
        email["To"] = recipient
        email["Subject"] = subject
        email.set_content(message)

        self.smtp_service.send_email(email)

    def _validate_email(self, recipient: str) -> bool:
        return "@" in recipient and "." in recipient
