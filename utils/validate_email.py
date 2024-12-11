import re


def validate_email(email: str) -> bool:
    """Validate the email address format using a regex."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return re.match(pattern, email) is not None
