from .models import User
from sqlmodel import Session

def get_user_by_id(session: Session, id: int) -> User | None:
    return session.get(User, id)