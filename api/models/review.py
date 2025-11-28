from sqlalchemy import Column, ForeignKey, Integer, String, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # You can link a review to an order OR a specific sandwich/menu_item
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)

    rating = Column(Integer, nullable=False)  # e.g., 1 to 5
    comment = Column(String(500))
    review_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))

    # Relationships
    user = relationship("User", back_populates="reviews")
    orders = relationship("Order", back_populates="reviews")