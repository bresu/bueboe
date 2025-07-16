# test v2/auth/login
import pytest
from fastapi.testclient import TestClient

def test_login_success(client, admin_user):
    """Test successful login with admin credentials"""
    response = client.post(
        "/v2/auth/login",
        json={"username": "admin", "password": "admin"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_password(client, admin_user):
    """Test login with invalid password"""
    response = client.post(
        "/v2/auth/login",
        json={"username": "admin", "password": "wrong"}
    )
    assert response.status_code == 401

def test_login_invalid_username(client, admin_user):
    """Test login with invalid username"""
    response = client.post(
        "/v2/auth/login",
        json={"username": "nonexistent", "password": "admin"}
    )
    assert response.status_code == 401

def test_get_current_user(client, admin_user):
    """Test getting current user with valid token"""
    login_response = client.post(
        "/v2/auth/login",
        json={"username": "admin", "password": "admin"}
    )
    token = login_response.json()["access_token"]

    response = client.get(
        "/v2/auth/user",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    print(f"{"+-"*5} Response: {data}")
    assert data["username"] == "admin"

def test_get_current_user_invalid_token(client, admin_user):
    """Test getting current user with invalid token"""
    response = client.get(
        "/v2/auth/user",
        headers={"Authorization": "Bearer invalidtoken"}
    )
    print(f"{"+"*10}Response:{response.json()}")
    assert response.status_code == 401