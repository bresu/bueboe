import pytest
from sqlmodel import SQLModel, Session, create_engine
from fastapi.testclient import TestClient
from main import app
from app.db.session import get_session
from app.db.models import User, Role
from app.core import security
from app.schemas.user import RoleName


# 1. Create an in-memory SQLite engine
@pytest.fixture(scope="session")
def test_engine():
    """Create a test database engine"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        # Echo SQL for debugging
        echo=True
    )
    return engine


# 2. Create and drop tables between tests
@pytest.fixture(autouse=True)
def setup_database(test_engine):
    """Create all tables before each test and drop them after"""
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)


# 3. Provide a session for use in tests
@pytest.fixture
def session(test_engine):
    """Create a new database session for a test"""
    with Session(test_engine) as session:
        yield session


# 4. Override the get_session dependency
@pytest.fixture
def client(session):
    """Create a test client with the session override"""
    def get_test_session():
        yield session

    app.dependency_overrides[get_session] = get_test_session
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# 5. Create admin user fixture
@pytest.fixture
def admin_user(session):
    """Create an admin role and user for testing"""
    # Create admin role
    role = Role(name=RoleName.ADMIN)
    session.add(role)
    session.commit()
    session.refresh(role)

    # Create admin user
    admin = User(
        username="admin",
        password_hash=security.hash_password("admin"),
        role_id=role.id
    )
    session.add(admin)
    session.commit()
    session.refresh(admin)

    return admin
