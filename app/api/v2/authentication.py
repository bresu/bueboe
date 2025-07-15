from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.schemas import auth as auth_schemas
import app.core.security as security
from sqlmodel import Session, select
from app.db.session import get_session
from app.db.models import User, Role
from app.schemas.user import UserRead, RoleName
router = APIRouter(prefix="/auth")

@router.post("/login",
                response_model=auth_schemas.TokenData,
                tags=["authentication"],
                status_code=status.HTTP_200_OK,
             )
def login(
        item: auth_schemas.LoginForm,
        session: Session = Depends(get_session)):
    """
    Expects username and password.
    Returns JWT token if credentials are valid.
    """
    # Here you would typically check the username and password against your database

    # hash pw and lookup if its valid with user

    user: User = session.exec(select(User).where(User.username == item.username)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        if not security.verify_password(item.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            # If the credentials are valid, create a token
            access_token = security.create_access_token(
                data={
                    "user_id": user.id,
                    "role": user.role.id,  # todo: id hier lassen?
                    "username": user.username, # brauch ma?
            })

            return {"access_token": access_token, "token_type": "bearer"}
        # needed testcases:
        # wrong username, wrong password
        # correct username, wrong password
        # wring uername, correct password
        # correct username, correct password

@router.get("/user",
            response_model=UserRead,
            tags=["authentication"])
def get_current_user(
        session: Session = Depends(get_session),
        user: User = Depends(security.get_current_user)):
    """
    Returns the current user by taking the JWT token from the request header.
    """
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get fresh user data with role
    stmt = select(User, Role).join(Role).where(User.id == user.id)
    result = session.exec(stmt).first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user, role = result
    # Convert to UserRead schema
    return UserRead(
        id=user.id,
        username=user.username,
        role_id=user.role_id,
        role_name=role.name
    )
