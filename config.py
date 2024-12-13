import os
from typing import List

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class AppConfig(BaseSettings):
    """Base configuration settings."""

    # General settings

    env: str = os.getenv("ENV", "dev")
    api: str = "/api"
    prefix: str = "/api/v1"
    project_name: str = "APIs Characters"

    datetime_format: str = "%Y-%m-%dT%H:%M:%S"
    date_format: str = "%Y-%m-%d"

    project_root: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # AUTH
    secret_key: str = os.getenv("SECRET_KEY")
    access_token_expire: int = 60 * 24 * 30  # 60 minutes * 24 hours * 30 days = 30 days

    backend_cors_origins: List[str] = ["*"]

    # Database settings
    engine: str = os.getenv("ENGINE", "postgresql")
    user: str = os.getenv("POSTGRES_USER", "postgres")
    password: str = os.getenv("POSTGRES_PASSWORD", "password")
    database_name: str = os.getenv("POSTGRES_DB", "characters_db")
    host: str = os.getenv("POSTGRES_HOST", "localhost")
    port: int = int(os.getenv("POSTGRES_PORT", 5432))
    database_url: str = f"{engine}://{user}:{password}@{host}:{port}/{database_name}"
    rabbit_user: str = os.getenv("RABBITMQ_DEFAULT_USER")
    rabbit_pass: str = os.getenv("RABBITMQ_DEFAULT_PASS")
    rabbit_host: str = "rabbitmq"
    rabbit_url: str = f"amqp://{rabbit_user}:{rabbit_pass}@{rabbit_host}:5672"
    characters_queue: str = os.getenv("CHARACTERS_QUEUE")
    exchange: str = os.getenv("EXCHANGE")
    routing_key: str = os.getenv("ROUTING_KEY")

    # SMTP settings
    smtp_server: str = os.getenv("SMTP_SERVER", "smtp.example.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", 587))
    smtp_username: str = os.getenv("SMTP_USERNAME")
    smtp_password: str = os.getenv("SMTP_PASSWORD")

    # Template and email
    template_dir: str = os.getenv("TEMPLATE_DIR")
    sendgrid_api_key: str = os.getenv("SENDGRID_API_KEY")
    sendgrid_default_sender: str = os.getenv("SENDGRID_DEFAULT_SENDER")


class TestConfig(AppConfig):
    """Test configuration settings."""
    env: str = "test"
    sqlite_file_name: str = "character.db"
    database_url: str = f"sqlite:///{sqlite_file_name}"

def get_settings() -> AppConfig:
    env = os.getenv("ENV", "dev")
    if env == "test":
        return TestConfig()
    return AppConfig()

settings = get_settings()
