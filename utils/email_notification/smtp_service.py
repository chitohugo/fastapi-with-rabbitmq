import smtplib
from email.message import EmailMessage


class SMTPService:
    def __init__(self, smtp_server: str, smtp_port: int, smtp_username: str, smtp_password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = smtp_username
        self.password = smtp_password

    def send_email(self, email: EmailMessage) -> None:
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(email)
            print(f"Email sent to {email['To']}.")
        except Exception as e:
            print(f"Error sending email: {e}")
            raise
