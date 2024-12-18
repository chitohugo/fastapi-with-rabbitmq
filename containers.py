from dependency_injector import containers, providers
from jinja2 import Environment, FileSystemLoader

from config import AppConfig
from core.repository.character_repository import CharacterRepository
from core.repository.user_repository import UserRepository
from core.services.auth_service import AuthService
from core.services.character_service import CharacterService
from core.services.rabbitmq_service import RabbitMQService
from core.services.user_service import UserService
from db.database import Database
from utils.email_notification.send_email import EmailNotification
from utils.email_notification.sendgrid import SendGridEmailService
from utils.email_notification.smtp_service import SMTPService
from utils.rabbitmq.consumer import RabbitMQConsumer
from utils.rabbitmq.manager import RabbitMQManager
from utils.rabbitmq.process_message import ProcessMessage
from utils.rabbitmq.producer import RabbitMQProducer


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[AppConfig()])

    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.endpoints.auth",
            "app.api.endpoints.users",
            "app.api.endpoints.characters",
            "core.dependencies"
        ]
    )

    db = providers.Singleton(Database, db_url=config.database_url)
    rabbitmq = providers.Singleton(RabbitMQManager, url=config.rabbit_url)
    rabbitmq_producer = providers.Factory(RabbitMQProducer, rabbitmq_manager=rabbitmq)

    user_repository = providers.Factory(UserRepository, session_factory=db.provided.session)
    character_repository = providers.Factory(CharacterRepository, session_factory=db.provided.session)

    auth_service = providers.Factory(AuthService, user_repository=user_repository)
    user_service = providers.Factory(UserService, user_repository=user_repository)
    character_service = providers.Factory(CharacterService, character_repository=character_repository)
    rabbitmq_service = providers.Factory(RabbitMQService, producer=rabbitmq_producer)

    # SMTP service configured
    smtp_service = providers.Factory(
        SMTPService,
        smtp_server=config.smtp_server,
        smtp_port=config.smtp_port,
        smtp_username=config.smtp_username,
        smtp_password=config.smtp_password,
    )
    # Sendgrid service configured
    sendgrid_service = providers.Singleton(
        SendGridEmailService,
        api_key=config.sendgrid_api_key,
        sender=config.sendgrid_default_sender
    )
    # Jinja2 environment configuration
    jinja2_service = providers.Singleton(
        Environment,
        loader=providers.Factory(FileSystemLoader, config.template_dir)
    )
    # Email notification service that uses the SMTP service
    email_service = providers.Factory(
        EmailNotification,
        service=sendgrid_service,
        template_env=jinja2_service
    )
    messages = providers.Factory(ProcessMessage, email_service=email_service)
    rabbitmq_consumer = providers.Factory(
        RabbitMQConsumer, manager=rabbitmq, callback=messages
    )
