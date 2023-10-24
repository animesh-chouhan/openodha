from enum import Enum
from pydantic import BaseModel


class PassStoreTypes(str, Enum):
    plaintext = "plaintext"
    bcrypt_hash = "bcrypt_hash"


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    pass_store_type: PassStoreTypes


class UserLogin(UserBase):
    password: str


class User(UserBase):
    user_id: str
    is_authenticated: bool
    api_key: str | None


class APIToken(BaseModel):
    api_token: str


class UserLogout(BaseModel):
    status: str
