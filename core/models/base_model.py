from sqlalchemy import Column, Integer, DateTime, func

from db.database import BaseModel


class Base(BaseModel):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

