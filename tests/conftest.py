import pytest
from sqlmodel import SQLModel, Session, create_engine
from fastapi.testclient import TestClient
from main import app
from app.db.session import get_session


# 1. Create an in-memory SQLite engine
@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    return engine


# 2. Provide a session for use in tests
@pytest.fixture
def session(test_engine):
    with Session(test_engine) as session:
        yield session

# 3. Override the app's session dependency for the tests
@pytest.fixture
def client(session):
    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    return TestClient(app)
