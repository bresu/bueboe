import pytest
from jose import jwt

import app.core.security as security

def test_jwt_token_creation():
    token = security.create_access_token(data={"sub": "test"})
    assert isinstance(token, str)
    assert len(token) > 0

def test_jwt_token_decode():
    token = security.create_access_token(data={"sub": "test"})
    print(f"Token: {token}")
    decoded = jwt.decode(token, security.settings.secret_key, algorithms=[security.ALGORITHM])
    assert decoded["sub"] == "test"

def test_jwt_token_expiration():
    token = security.create_access_token(data={"sub": "test"}, expires_delta=1)
    decoded = jwt.decode(token, security.settings.secret_key, algorithms=[security.ALGORITHM])
    print(f"Decoded: {decoded}")
    assert "exp" in decoded
    assert decoded["sub"] == "test"

def test_jwt_token_invalid_signature():
    token = security.create_access_token(data={"sub": "test"})
    with pytest.raises(jwt.JWTError):
        jwt.decode(token, "wrong_secret_key", algorithms=[security.ALGORITHM])

def test_jwt_token_missing_subject():
    with pytest.raises(jwt.JWTError):
        jwt.decode("invalid_token", security.settings.secret_key, algorithms=[security.ALGORITHM])

def test_jwt_token_with_expired_token():
    token = security.create_access_token(data={"sub": "test"}, expires_delta=-1)
    with pytest.raises(jwt.ExpiredSignatureError):
        jwt.decode(token, security.settings.secret_key, algorithms=[security.ALGORITHM])

