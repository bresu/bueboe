from pydantic import BaseModel, computed_field
from enum import Enum
from typing import Optional

class RoleName(str, Enum):
    ADMIN = "admin"
    MANDATE = "mandate"
    VOLUNTEER = "volunteer"

class UserCreate(BaseModel):
    username: str
    # email: str
    password: str
    role_name: RoleName

class UserRead(BaseModel):
    id: int
    username: str
    role_id: int
    role_name: Optional[RoleName] = None

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }
