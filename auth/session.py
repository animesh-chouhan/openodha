import redis
from pydantic import BaseModel

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

SESSION_DURATION = 6 * 60 * 60


class Session(BaseModel):
    user_id: str
    session_id: str | None


def create_session(user_id) -> Session:
    session_id = "asd123"
    session = Session(user_id=user_id, session_id=session_id)
    r.set(user_id, session_id, SESSION_DURATION)
    return session


def get_session(user_id) -> Session:
    session_id = r.get(user_id)
    if session_id:
        session = Session(user_id=user_id, session_id=session_id)
        return session
    return None


def delete_session(user_id):
    r.delete(user_id)
