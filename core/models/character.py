from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship

from .base_model import Base


class Character(Base):
    __tablename__ = "characters"

    name = Column(String, unique=True, nullable=False)
    height = Column(Float, nullable=False)
    mass = Column(Float, nullable=False)
    hair_color = Column(String, nullable=False)
    skin_color = Column(String, nullable=False)
    eye_color = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", backref="characters")
