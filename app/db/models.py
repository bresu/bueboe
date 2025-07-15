from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.schemas.user import RoleName  # From schemas/role.py


class Role(SQLModel, table=True):
    __tablename__ = "roles"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: RoleName = Field(sa_column=Column(String(20), unique=True, nullable=False))

    users: List["User"] = Relationship(back_populates="role")


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(nullable=False, unique=True)
    # email: str = Field(nullable=False, unique=True) # not needed probably, because we cant send emails
    password_hash: str = Field(nullable=False)

    role_id: int = Field(foreign_key="roles.id", nullable=False)
    role: Optional[Role] = Relationship(back_populates="users")
