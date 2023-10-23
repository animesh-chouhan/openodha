from sqlalchemy.orm import Session
import uuid

import models, schemas, utils
from session import get_session, delete_session


def update_auth_status_login(db, db_user):
    if not db_user.is_authenticated:
        db_user.is_authenticated = True
        db.commit()
        db.refresh(db_user)
    return db_user


def update_auth_status_logout(db, db_user):
    if db_user.is_authenticated:
        db_user.is_authenticated = False
        db.commit()
        db.refresh(db_user)
    return db_user


def create_user(db: Session, user: schemas.UserCreate):
    user_id = str(uuid.uuid4())
    username = user.username
    password = user.password
    pass_store_type = user.pass_store_type

    match pass_store_type:
        case "plaintext":
            stored_password = password

        case "bcrypt_hash":
            stored_password = utils.bcrypt_hash_password(password)

    db_user = models.User(
        user_id=user_id,
        username=username,
        password=stored_password,
        pass_store_type=pass_store_type,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def user_login(db, username, password):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user:
        stored_password = db_user.password
        auth_status = False
        match db_user.pass_store_type:
            case "plaintext":
                if stored_password == password:
                    auth_status = True

            case "bcrypt_hash":
                if utils.bcrypt_check_password(password, stored_password):
                    auth_status = True
        if auth_status:
            db_user = update_auth_status_login(db, db_user)
            return db_user
    else:
        return None


def user_logout(db, user_id, session_id):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user:
        session = get_session(user_id)
        if session:
            delete_session(user_id)
            db_user = update_auth_status_logout(db, db_user)
            return db_user
        return None
    else:
        return None
