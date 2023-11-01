import secrets
from decimal import Decimal, getcontext
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from fastapi.security import APIKeyQuery

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
query_scheme = APIKeyQuery(name="api_key")
getcontext().prec = 2


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/portfolio")
def get_portfolio(api_key: str = Depends(query_scheme)):
    return api_key


@app.post("/api/update-balance")
def update_balance(api_key: str = Depends(query_scheme)):
    pass


@app.post("/api/orders")
def place_order(api_key: str = Depends(query_scheme)):
    pass


@app.get("/api/orders")
def get_orders(api_key: str = Depends(query_scheme)):
    pass


@app.get("/api/trades")
def place_order(api_key: str = Depends(query_scheme)):
    pass
