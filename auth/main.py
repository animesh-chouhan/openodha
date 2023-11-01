import os
import secrets
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status, Cookie
from sqlalchemy.orm import Session

# from starlette_csrf import CSRFMiddleware
# from fastapi.security import APIKeyQuery

import crud, models, schemas
from database import SessionLocal, engine
from session import (
    UserSession,
    create_session,
    get_session,
    delete_session,
    SESSION_DURATION,
)

models.Base.metadata.create_all(bind=engine)

if os.environ.get("APP_ENV") == "PROD":
    root_path = "/auth"
else:
    root_path = ""


app = FastAPI(
    title="Openodha Auth",
    summary="Authentication API for Openodha",
    version="0.0.1",
    license_info={
        "name": "Apache 2.0",
        "url": "http://www.apache.org/licenses/LICENSE-2.0",
    },
    root_path=root_path,
    openapi_url="/openapi.json",
)
# app.add_middleware(CSRFMiddleware, secret=secrets.token_hex(32))
# query_scheme = APIKeyQuery(name="api_key")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_session(user_id: str | None, session_id: str | None) -> UserSession:
    error = False
    if user_id:
        session = get_session(user_id)
        if session and session.session_id == session_id:
            return session
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized session",
    )


@app.get("/health", response_model=schemas.HealthCheck)
def health():
    return schemas.HealthCheck(status="OK")


@app.post("/users", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    else:
        return crud.create_user(db=db, user=user)


@app.post("/login", response_model=schemas.User)
def login(user: schemas.UserLogin, response: Response, db: Session = Depends(get_db)):
    db_user = crud.user_login(db, username=user.username, password=user.password)
    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid username/password")

    response.set_cookie(key="user_id", value=db_user.user_id)
    session = create_session(db_user.user_id)
    response.set_cookie(
        key="session_id", value=session.session_id, max_age=SESSION_DURATION
    )
    return db_user


@app.post("/api-key", response_model=schemas.APIKey)
def generate_api_key(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    session_id = request.cookies.get("session_id")
    session = get_user_session(user_id, session_id)
    if session:
        db_user = crud.get_user_by_user_id(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        api_key = secrets.token_urlsafe(32)
        db_user = crud.set_user_token(db, db_user, api_key)
        return db_user


@app.get("/api-key", response_model=schemas.APIKey)
def get_api_key(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    session_id = request.cookies.get("session_id")
    session = get_user_session(user_id, session_id)
    if session:
        db_user = crud.get_user_by_user_id(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        if db_user.api_key:
            return db_user
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No API token found",
        )


@app.get("/users", response_model=list[schemas.User])
def read_users(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    user_id = request.cookies.get("user_id")
    session_id = request.cookies.get("session_id")
    session = get_user_session(user_id, session_id)
    if session:
        users = crud.get_users(db, skip=skip, limit=limit)
        return users


@app.get("/users/{username}", response_model=schemas.User)
def read_user(request: Request, username: str, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    session_id = request.cookies.get("session_id")
    session = get_user_session(user_id, session_id)
    if session:
        db_user = crud.get_user_by_username(db, username=username)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user


@app.post("/logout", response_model=schemas.UserLogout)
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    session_id = request.cookies.get("session_id")
    session = get_user_session(user_id, session_id)
    if session:
        db_user = crud.user_logout(db, user_id=user_id)
        if db_user is None:
            return {"status": "User invalid/already logged out"}
        response.set_cookie(key="session_id", expires="Thu, 01 Jan 1970 00:00:01 GMT")
        delete_session(user_id)
        return {"status": "User successfully logged out"}
