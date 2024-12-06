from core.exceptions import AuthError
from core.security import ALGORITHM, JWTBearer
from core.services.user_service import UserService
from core.models.user import User
from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from config import settings
from container import Container
from core.schema.auth_schema import Payload
from jose import jwt
from pydantic import ValidationError


@inject
def get_current_user(
        token: str = Depends(JWTBearer()),
        service: UserService = Depends(Provide[Container.user_service]),
) -> User:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=ALGORITHM)
        token_data = Payload(**payload)
    except (jwt.JWTError, ValidationError):
        raise AuthError(message="Could not validate credentials")

    current_user = service.get_by_field("id", token_data.id)
    if not current_user:
        raise AuthError(message="Lead not found")

    return current_user
