from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

# from fastapi.security import APIKeyQuery

import crud, models, schemas
from database import SessionLocal, engine
from session import create_session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# query_scheme = APIKeyQuery(name="api_key")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
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
    response.set_cookie(key="session_id", value=session.session_id)
    return db_user


@app.post("/api-key", response_model=schemas.APIToken)
def get_api_key():
    pass


@app.get("/users", response_model=list[schemas.User] | schemas.User)
def read_users(
    user_id: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    if user_id == None:
        users = crud.get_users(db, skip=skip, limit=limit)
        return users
    else:
        db_user = crud.get_user(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user


@app.get("/users/{username}", response_model=schemas.User)
def read_user(username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/logout", response_model=schemas.User, status_code=200)
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    session_id = request.cookies.get("session_id")
    db_user = crud.user_logout(db, user_id=user_id, session_id=session_id)
    if db_user is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"status": "User invalid/already logged out"}
    return db_user
