from core.schema.base_schema import ModelBaseInfo
from pydantic import BaseModel, Field


class BaseCharacter(BaseModel):
    name: str
    height: float
    mass: float
    hair_color: str
    skin_color: str
    eye_color: str

    class Config:
        from_attributes = True


class Character(ModelBaseInfo, BaseCharacter):
    ...


class PostCharacter(BaseCharacter):
    user_id: int = None
    ...


class UpdateCharacter(BaseCharacter):
    ...
