from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail



class OrderBase(BaseModel):
    user_id: int
    description: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    user_id: Optional[int] = None
    description: Optional[str] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    order_details: list[OrderDetail] = None

    class ConfigDict:
        from_attributes = True
