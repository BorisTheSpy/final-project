from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class PaymentBase(BaseModel):
    amount: float
    payment_method: str
    transaction_status: Optional[str] = "Completed"


class PaymentCreate(PaymentBase):
    order_id: int


class PaymentUpdate(BaseModel):
    amount: Optional[float] = None
    payment_method: Optional[str] = None
    transaction_status: Optional[str] = None


class Payment(PaymentBase):
    id: int
    order_id: int
    payment_date: Optional[datetime] = None

    class ConfigDict:
        from_attributes = True