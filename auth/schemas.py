from enum import Enum
from pydantic import BaseModel


class HealthCheck(BaseModel):
    status: str = "OK"


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserLogin(UserBase):
    password: str


class User(UserBase):
    user_id: str
    api_key: str | None


class APIKey(BaseModel):
    api_key: str


class UserLogout(BaseModel):
    status: str
