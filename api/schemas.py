from typing import List, Optional
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime


class User(BaseModel):
    user_id: str
    username: str
    api_key: str | None


class Holding(BaseModel):
    symbol: str
    quantity: int
    price: Decimal


class UserProfile(User):
    balance: Decimal
    holdings: Optional[List[Holding]]


class Order(BaseModel):
    user_id: str
    order_id: str
    order_type: str
    exchange: str
    order_timestamp: datetime
    symbol: str
    transaction_type: str
    quantity: int
    price: Decimal
    average_price: Decimal
    filled_quantity: int
    pending_quantity: int


class Trade(BaseModel):
    trade_id: str
    order_id: str
    exchange: str
    fill_timestamp: datetime
    symbol: str
    transaction_type: str
    quantity: int
    average_price: Decimal
