from sqlalchemy.orm import Session
import uuid

import models, schemas, utils
from session import get_session, delete_session


def create_user(db: Session, user: schemas.UserCreate):
    user_id = str(uuid.uuid4())
    username = user.username
    password = user.password
    stored_password = utils.bcrypt_hash_password(password)

    db_user = models.User(user_id=user_id, username=username, password=stored_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_user_id(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def user_login(db, username, password):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user:
        stored_password = db_user.password
        if utils.bcrypt_check_password(password, stored_password):
            return db_user
    return None


def set_user_token(db, db_user, api_key):
    db_user.api_key = api_key
    db.commit()
    db.refresh(db_user)
    return db_user


def user_logout(db, user_id):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user:
        delete_session(user_id)
        return db_user
    else:
        return None
