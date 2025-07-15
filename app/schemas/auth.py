from pydantic import BaseModel

class LoginForm(BaseModel):
    username: str
    password: str

class TokenData(BaseModel):
    access_token: str
    token_type: str