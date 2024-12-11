import re
from email.message import EmailMessage
from typing import Any
from jinja2 import Environment

from logger_config import logger
from utils.email_notification.abstract_notification import NotificationServiceAbstract
from utils.email_notification.smtp_service import SMTPService


class EmailNotification(NotificationServiceAbstract):
    def __init__(self, smtp_service: SMTPService, template_env: Environment):
        self.smtp_service = smtp_service
        self.template_env = template_env

    async def send_notification(self, **kwargs) -> None:
        try:
            recipient = kwargs.pop("recipient")
            subject = kwargs.pop("subject", "No Subject")
            template_name = kwargs.pop("template_name")
            template_data = kwargs

            logger.info(f"Preparing to send email to: {recipient}")

            if not self._validate_email(recipient):
                raise ValueError(f"Invalid email address: {recipient}")

            # Render the email template
            rendered_html = self._render_template(template_name, template_data)

            # Prepare the email
            email = self._compose_email(recipient, subject, rendered_html)

            # Send the email
            logger.info(f"Sending email to: {recipient}")
            self.smtp_service.send_email(email)
            logger.info(f"Email successfully sent to: {recipient}")

        except KeyError as e:
            logger.error(f"Missing required parameter: {e}")
            raise ValueError(f"Missing required parameter: {e}")

    def _validate_email(self, email: str) -> bool:
        """Validate the email address format using a regex."""
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        return re.match(email_regex, email) is not None

    def _render_template(self, template_name: str, data: dict[str, Any]) -> str:
        """Render the email template with the given data."""
        try:
            template = self.template_env.get_template(template_name)
            rendered_html = template.render(**data)
            logger.debug(f"Rendered template for {template_name}: {rendered_html}")
            return rendered_html
        except Exception as e:
            logger.error(f"Error rendering template {template_name}: {e}")
            raise ValueError("Failed to render email template.")

    def _compose_email(self, recipient: str, subject: str, html_content: str) -> EmailMessage:
        """Compose the email with the provided details."""
        email = EmailMessage()
        email["From"] = self.smtp_service.username
        email["To"] = recipient
        email["Subject"] = subject
        email.add_alternative(html_content, subtype="html")
        return email
