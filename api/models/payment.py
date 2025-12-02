from sqlalchemy import Column, ForeignKey, Integer, DECIMAL, String, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)

    amount = Column(DECIMAL(10, 2), nullable=False)
    payment_method = Column(String(50))  # e.g., 'Credit Card', 'Cash', 'Token'
    transaction_status = Column(String(50), default="Completed")
    payment_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))

    # Relationship
    orders = relationship("Order", back_populates="payment")