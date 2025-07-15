from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, UserRead
from app.db.models import User, Role
from app.core import security
from sqlmodel import Session, select
from app.db.session import get_session
import app.api.v2.authentication as auth
#from sqlmodel import selectinload

router = APIRouter(prefix="/v2")
router.include_router(auth.router, tags=["auth"])

@router.get("/")
def root():
    return {"message": "Hello, FastAPI"}

@router.get("/hello/{name}")
async def say_hello(name: str):
     return {"message": f"Hello {name}"}

# endpoints for user
@router.post("/users",
             response_model=UserRead,
             tags=["users"],
             status_code=201,
             dependencies=[Depends(security.require_admin)])
def create_user(
    payload: UserCreate,
    session : Session = Depends(get_session),
    ):
    """
    Create a new user with the given payload. Only users who are admins can create new users.
    """
    if session.exec(select(User).where(User.username == payload.username)).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )
    role = session.exec(select(Role).where(Role.name == payload.role_name)).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role {payload.role_name} not found",
        )

    user = User(
        username=payload.username,
        password_hash=security.hash_password(payload.password),
        role_id=role.id,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    # Reload the user with role relationship
    #return session.exec(select(User).where(User.id == user.id).options(selectinload(User.role))).first()
    return None

# endpoint for roles

# endpoint for users

# endpoint for books

# endpoint for sellers

# endpoint for offers

# endpoint for transactions
