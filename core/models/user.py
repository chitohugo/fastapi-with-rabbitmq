from sqlalchemy import Column, String

from .base_model import Base


class User(Base):
    __tablename__ = "users"

    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    password = Column(String, nullable=False)

