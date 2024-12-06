from contextlib import AbstractContextManager
from typing import Callable

from core.models.user import User
from core.repository.base_repository import BaseRepository
from sqlalchemy.orm import Session


class UserRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, User)
