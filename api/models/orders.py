from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    description = Column(String(300))

    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))

    tracking_number = Column(String(50))
    status = Column(String(50), default="Placed")

    order_details = relationship("OrderDetail", back_populates="order")
    payment = relationship("Payment", uselist=False, back_populates="order")
    review = relationship("Review", uselist=False, back_populates="order")
    user = relationship("User", back_populates="orders")