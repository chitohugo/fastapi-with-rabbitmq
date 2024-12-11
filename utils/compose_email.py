from email.message import EmailMessage

from utils.email_notification.smtp_service import SMTPService


def compose_email(smtp_service: SMTPService, recipient: str, subject: str, html_content: str) -> EmailMessage:
    """Compose the email with the provided details."""
    email = EmailMessage()
    email["From"] = smtp_service.username
    email["To"] = recipient
    email["Subject"] = subject
    email.add_alternative(html_content, subtype="html")
    return email
