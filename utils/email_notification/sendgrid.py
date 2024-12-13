from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, Content

from utils.email_notification.abstract_service_email import EmailServiceAbstract


class SendGridEmailService(EmailServiceAbstract):
    def __init__(self, api_key: str, sender: str):
        self.client = SendGridAPIClient(api_key)
        self.sender = sender

    def send_email(self, recipient: str, subject: str, rendered_html: str, is_html: bool = False):
        content_type = "text/html" if is_html else "text/plain"
        message = Mail(
            from_email=Email(self.sender),
            to_emails=recipient,
            subject=subject,
            html_content=Content(content_type, rendered_html),
        )
        try:
            response = self.client.send(message)
            return {
                "status_code": response.status_code,
                "body": response.body.decode("utf-8"),
                "headers": response.headers,
            }
        except Exception as e:
            return {"error": str(e)}
