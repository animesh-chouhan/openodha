import os
import secrets
import redis
from pydantic import BaseModel

redis_host = os.environ.get("DOCKER_HOST", "localhost")
password_location = os.environ.get("REDIS_PASSWORD_LOC")
in_docker = os.environ.get("IN_DOCKER") == "True"

if in_docker:
    with open(password_location) as f:
        redis_password = f.read()
else:
    redis_password = os.environ.get("REDIS_PASSWORD")

r = redis.Redis(
    host=redis_host,
    port=6379,
    decode_responses=True,
    username="default",
    password=redis_password,
)

SESSION_DURATION = 6 * 60 * 60


class UserSession(BaseModel):
    user_id: str
    session_id: str | None


def create_session(user_id) -> UserSession:
    session_id = secrets.token_urlsafe(32)
    session = UserSession(user_id=user_id, session_id=session_id)
    r.set(user_id, session_id, SESSION_DURATION)
    return session


def get_session(user_id) -> UserSession:
    session_id = r.get(user_id)
    if session_id:
        session = UserSession(user_id=user_id, session_id=session_id)
        return session
    return None


def delete_session(user_id):
    r.delete(user_id)
