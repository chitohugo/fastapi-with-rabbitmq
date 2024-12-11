import os
from email.message import EmailMessage

from jinja2 import Environment, FileSystemLoader
from logger_config import logger
from utils.email_notification.abstract_notification import NotificationServiceAbstract
from utils.email_notification.smtp_service import SMTPService


class EmailNotification(NotificationServiceAbstract):
    def __init__(self, smtp_service: SMTPService, template_dir: str):
        self.smtp_service = smtp_service
        self.template_env = Environment(loader=FileSystemLoader(template_dir))

    async def send_notification(
        self,
        **kwargs,
    ) -> None:
        recipient = kwargs.pop("recipient")
        subject = kwargs.get("subject")
        template_name = kwargs.pop("template_name")
        template_data = kwargs

        logger.info(f"Sending email to: {recipient}")
        logger.info(f"Subject: {subject}")
        if not self._validate_email(recipient):
            raise ValueError("The email recipient is invalid.")

        logger.info(f"Sending email to: {kwargs}")

        # Render the HTML template
        html_template = self.template_env.get_template(template_name)
        rendered_html = html_template.render(**template_data)
        logger.info(f"Rendered HTML: {rendered_html}")

        email = EmailMessage()
        email["From"] = self.smtp_service.username
        email["To"] = recipient
        email["Subject"] = subject
        email.add_alternative(rendered_html, subtype="html")

        self.smtp_service.send_email(email)

    def _validate_email(self, recipient: str) -> bool:
        return "@" in recipient and "." in recipient
