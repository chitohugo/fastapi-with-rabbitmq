from datetime import timedelta

from core.exceptions import AuthError
from core.models.user import User
from core.security import create_access_token, get_password_hash, verify_password
from core.repository.user_repository import UserRepository
from config import settings
from core.schema.auth_schema import Payload, SignIn, SignUp


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository

    async def get_list(self):
        return await self.repository.read()

    async def add(self, schema):
        return await self.repository.create(schema)

    async def patch(self, id: int, schema):
        return await self.repository.update(id, schema)

    async def remove_by_id(self, id):
        return await self.repository.delete_by_id(id)

    async def sign_in(self, sign_in: SignIn):
        user: User = await self.repository.read_by_field("email", sign_in.email)
        if not user:
            raise AuthError(message="Incorrect email or password")

        if not verify_password(sign_in.password, user.password):
            raise AuthError(message="Incorrect password")

        payload = Payload(
            id=user.id,
            email=user.email,
            first_name=user.first_name
        )
        token_lifespan = timedelta(minutes=settings.access_token_expire)
        access_token, expiration_datetime = create_access_token(payload.model_dump(), token_lifespan)
        response = {
            "access_token": access_token
        }
        return response

    async def sign_up(self, user: SignUp):
        # user = User(**sign_up.dict(exclude_none=True))
        user.password = get_password_hash(user.password)
        created = await self.repository.create(user)
        return created

