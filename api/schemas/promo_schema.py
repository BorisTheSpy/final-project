from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class PromoBase(BaseModel):
    code: str
    description: Optional[str] = None
    discount_type: str
    value: float
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class PromoCreate(PromoBase):
    pass


class PromoUpdate(BaseModel):
    code: Optional[str] = None
    description: Optional[str] = None
    discount_type: Optional[str] = None
    value: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[int] = None


class Promo(PromoBase):
    id: int
    is_active: int

    class ConfigDict:
        from_attributes = True