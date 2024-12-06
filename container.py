from dependency_injector import containers, providers

from config import settings
from core.repository.character_repository import CharacterRepository
from core.repository.user_repository import UserRepository
from core.services.auth_service import AuthService
from core.services.character_service import CharacterService
from core.services.rabbitmq_service import RabbitMQService
from core.services.user_service import UserService
from db.database import Database
from utils.rabbitmq.manager import RabbitMQManager
from utils.rabbitmq.producer import RabbitMQProducer


class Container(containers.DeclarativeContainer):
    # config = providers.Configuration(pydantic_settings=[Configs()])

    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.endpoints.auth",
            "app.api.endpoints.users",
            "app.api.endpoints.characters",
            "core.dependencies"
        ]
    )

    db = providers.Singleton(Database, db_url=settings.database_url)
    rabbitmq = providers.Singleton(RabbitMQManager, url=settings.rabbit_url)
    rabbitmq_producer = providers.Factory(RabbitMQProducer, rabbitmq_manager=rabbitmq)

    user_repository = providers.Factory(UserRepository, session_factory=db.provided.session)
    character_repository = providers.Factory(CharacterRepository, session_factory=db.provided.session)

    auth_service = providers.Factory(AuthService, user_repository=user_repository)
    user_service = providers.Factory(UserService, user_repository=user_repository)
    character_service = providers.Factory(CharacterService, character_repository=character_repository)
    rabbitmq_service = providers.Factory(RabbitMQService, producer=rabbitmq_producer)

