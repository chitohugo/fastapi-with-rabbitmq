from datetime import datetime

from pydantic import BaseModel


class ModelBaseInfo(BaseModel):
    id: int = None
    created_at: datetime
    updated_at: datetime


class Blank(BaseModel):
    pass
