from os import environ
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
environ["APP_ENV"] = "test"

@pytest.fixture(scope='module')
def app() -> FastAPI:
    from app.main import get_application

    return get_application()


@pytest.fixture(scope='module')
def test_app(app):
    client = TestClient(app)
    yield client
