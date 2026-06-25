import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database.base import Base
from app.database.session import get_db

# Setup in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    database = TestingSessionLocal()
    try:
        yield database
    finally:
        database.close()


@pytest.fixture(autouse=True)
def setup_db():
    # Create the tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop the tables
    Base.metadata.drop_all(bind=engine)


# Apply the dependency override
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_register_and_login():
    # 1. Register a new user
    reg_payload = {
        "email": "testuser@example.com",
        "password": "strongpassword123",
        "full_name": "Test User"
    }
    reg_response = client.post("/api/v1/auth/register", json=reg_payload)
    assert reg_response.status_code == 201
    user_data = reg_response.json()
    assert user_data["email"] == reg_payload["email"]
    assert user_data["full_name"] == reg_payload["full_name"]
    assert "id" in user_data
    assert user_data["is_active"] is True

    # 2. Try to register with same email (should fail)
    fail_reg = client.post("/api/v1/auth/register", json=reg_payload)
    assert fail_reg.status_code == 409

    # 3. Login with credentials
    login_payload = {
        "email": "testuser@example.com",
        "password": "strongpassword123"
    }
    login_response = client.post("/api/v1/auth/login", json=login_payload)
    assert login_response.status_code == 200
    tokens = login_response.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["token_type"] == "bearer"

    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]

    # 4. Get profile with access token
    headers = {"Authorization": f"Bearer {access_token}"}
    profile_response = client.get("/api/v1/auth/profile", headers=headers)
    assert profile_response.status_code == 200
    profile_data = profile_response.json()
    assert profile_data["email"] == "testuser@example.com"
    assert profile_data["full_name"] == "Test User"

    # 5. Refresh token
    refresh_headers = {"Authorization": f"Bearer {refresh_token}"}
    refresh_response = client.post("/api/v1/auth/refresh", headers=refresh_headers)
    assert refresh_response.status_code == 200
    new_tokens = refresh_response.json()
    assert "access_token" in new_tokens
    assert new_tokens["token_type"] == "bearer"

    # 6. Logout endpoint (stateless check)
    logout_response = client.post("/api/v1/auth/logout", headers=headers)
    assert logout_response.status_code == 200
    assert logout_response.json()["status"] == "logged_out"


def test_users_endpoints():
    # Register and login to get token
    reg_payload = {
        "email": "anotheruser@example.com",
        "password": "anotherpassword",
        "full_name": "Another User"
    }
    client.post("/api/v1/auth/register", json=reg_payload)

    login_response = client.post("/api/v1/auth/login", json={
        "email": "anotheruser@example.com",
        "password": "anotherpassword"
    })
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # 1. GET /api/v1/users/me
    get_response = client.get("/api/v1/users/me", headers=headers)
    assert get_response.status_code == 200
    assert get_response.json()["full_name"] == "Another User"

    # 2. PUT /api/v1/users/me
    put_payload = {
        "full_name": "Updated Name",
        "email": "updatedemail@example.com"
    }
    put_response = client.put("/api/v1/users/me", json=put_payload, headers=headers)
    assert put_response.status_code == 200
    assert put_response.json()["full_name"] == "Updated Name"
    assert put_response.json()["email"] == "updatedemail@example.com"

    # 3. DELETE /api/v1/users/me
    del_response = client.delete("/api/v1/users/me", headers=headers)
    assert del_response.status_code == 200
    assert del_response.json()["status"] == "deactivated"

    # 4. Try to access profile again (should fail because inactive)
    get_again = client.get("/api/v1/users/me", headers=headers)
    assert get_again.status_code == 403
