from jinja2 import Environment

from logger_config import logger
from utils.compose_email import compose_email
from utils.email_notification.abstract_notification import NotificationServiceAbstract
from utils.email_notification.smtp_service import SMTPService
from utils.render_template import render_template
from utils.validate_email import validate_email


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

            if not validate_email(recipient):
                raise ValueError(f"Invalid email address: {recipient}")

            # Render the email template
            rendered_html = render_template(self.template_env, template_name, template_data)

            # Prepare the email
            email = compose_email(self.smtp_service, recipient, subject, rendered_html)

            # Send the email
            logger.info(f"Sending email to: {recipient}")
            self.smtp_service.send_email(email)
            logger.info(f"Email successfully sent to: {recipient}")

        except KeyError as e:
            logger.error(f"Missing required parameter: {e}")
            raise ValueError(f"Missing required parameter: {e}")
