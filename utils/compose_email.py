from email.message import EmailMessage


def compose_email(sender: str, recipient: str, subject: str, html_content: str) -> EmailMessage:
    """Compose the email with the provided details."""
    email = EmailMessage()
    email["From"] = sender
    email["To"] = recipient
    email["Subject"] = subject
    email.add_alternative(html_content, subtype="html")
    return email
