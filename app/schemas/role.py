from pydantic import BaseModel
from .user import RoleName

class RoleBase(BaseModel):
    name: RoleName

class RoleCreate(RoleBase):
    pass

class RoleRead(RoleBase):
    id: int

    class Config:
        from_attributes = True  # For SQLAlchemy model compatibility
