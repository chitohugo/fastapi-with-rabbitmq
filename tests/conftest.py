import os

os.environ["ENV"] = "test"

from core.models.user import User
from db.database import BaseModel

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from core.security import get_password_hash
from config import settings
from main import AppCreator


@pytest.fixture(scope="function")
def session():
    engine = create_engine(settings.database_url)
    BaseModel.metadata.create_all(engine)

    session = Session(bind=engine)

    try:
        yield session
    finally:
        session.rollback()
        session.close()
        BaseModel.metadata.drop_all(engine)

@pytest.fixture
def client(session):
    app_creator = AppCreator()
    app = app_creator.app

    with TestClient(app) as client:
        yield client

@pytest.fixture
def create_user(session):
    data = {
        "email": "julian.clark@gmail.com",
        "username": "delicatesilk",
        "first_name": "Julian",
        "last_name": "Clark",
        "password": get_password_hash('dolor')
    }
    instance = User(**data)
    session.add(instance)
    session.commit()
    yield instance


@pytest.fixture
def auth_token(client):
    auth_data = {
        "email": "julian.clark@gmail.com",
        "password": "dolor"
    }
    response = client.post("/api/v1/auth/sign-in", json=auth_data)
    assert response.status_code == 200
    token = response.json().get("access_token")

    return token


@pytest.fixture
def req(session, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    app_creator = AppCreator()
    app = app_creator.app

    with TestClient(app) as client:
        client.headers.update(headers)
        yield client
