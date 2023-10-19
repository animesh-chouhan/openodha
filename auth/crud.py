from sqlalchemy.orm import Session
import uuid

import models, schemas, utils


def create_user(db: Session, user: schemas.UserCreate):
    userid = str(uuid.uuid4())
    username = user.username
    password = user.password
    pass_store_type = user.pass_store_type

    match pass_store_type:
        case "plaintext":
            stored_password = password

        case "bcrypt_hash":
            stored_password = utils.bcrypt_hash_password(password)

    db_user = models.User(
        userid=userid,
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


def get_user(db: Session, userid: str):
    return db.query(models.User).filter(models.User.userid == userid).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def user_login(db, username, password):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user:
        stored_password = db_user.password
        match db_user.pass_store_type:
            case "plaintext":
                if stored_password == password:
                    return db_user

            case "bcrypt_hash":
                if utils.bcrypt_check_password(password, stored_password):
                    return db_user
    else:
        return None
