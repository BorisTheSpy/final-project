from typing import Optional
from pydantic import BaseModel


class ReviewBase(BaseModel):
    rating: int # 1 to 5
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    user_id: int
    order_id: int


class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None


class Review(ReviewBase):
    id: int
    user_id: int
    order_id: Optional[int] = None

    class ConfigDict:
        from_attributes = True