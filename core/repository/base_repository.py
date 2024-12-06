from contextlib import AbstractContextManager
from typing import Callable

from core.exceptions import DuplicatedError, NotFoundError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


class BaseRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]], model) -> None:
        self.session_factory = session_factory
        self.model = model

    def read_by_field(self, field_name, value):
        with self.session_factory() as session:
            query = session.query(self.model)
            print(session.connection().engine)
            query = query.filter(getattr(self.model, field_name) == value).first()
            if not query:
                raise NotFoundError(message=f"Not found {field_name} : {value}")
            return query

    def read(self):
        with self.session_factory() as session:
            query = session.query(self.model)
            return query

    def create(self, schema):
        with self.session_factory() as session:
            try:
                query = self.model(**schema.model_dump(), id=None)
                session.add(query)
                session.commit()
                session.refresh(query)
            except IntegrityError as e:
                raise DuplicatedError(message="The value already exists") from e
            return query
    def update(self, id: int, schema):
        with self.session_factory() as session:
            session.query(self.model).filter(self.model.id == id).update(schema.model_dump(exclude_none=True))
            session.commit()
            return self.read_by_field("id", id)

    def delete_by_id(self, id: int):
        with self.session_factory() as session:
            query = session.query(self.model).filter(self.model.id == id).first()
            if not query:
                raise NotFoundError(message=f"not found id : {id}")
            session.delete(query)
            session.commit()
