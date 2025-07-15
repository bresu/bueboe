# app/core/security.py
from datetime import datetime, timedelta, UTC
from typing import Any, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from app.core.config import settings
from app.db.models import User
from app.db.session import get_session

# Hashing helpers
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(pw: str) -> str:
    return pwd_context.hash(pw)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# JWT helpers -------------------------------------------------------------
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MIN = 60  # minutes

def create_access_token(data: dict[str, Any], expires_delta: Optional[int] = None):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(
        minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MIN
    )
    to_encode.update({"exp": expire})
    to_encode.update({"iat": datetime.now(UTC)})
    return jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v2/auth/login") #TODO: check if this is correctly done

def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User: #FIXME: use UserRead instead of User?
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        user_id: int | None = payload.get("user_id")
        if user_id is None:
            raise credentials_exc
    except JWTError:
        raise credentials_exc

    user = session.get(User, user_id)
    if user is None:
        raise credentials_exc
    return user


def require_admin(user: User = Depends(get_current_user)):
    if user.role.name != "admin":
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource.")
    return user

def require_mandate(user: User = Depends(get_current_user)):
    if user.role.name not in ["admin", "mandate"]:
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource.")
    return user

def require_volunteer(user: User = Depends(get_current_user)):
    if user.role.name not in ["admin", "mandate", "volunteer"]:
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource.")
    return user