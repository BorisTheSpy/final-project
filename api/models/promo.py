from sqlalchemy import Column, Integer, String, DECIMAL, DATETIME
from datetime import datetime
from ..dependencies.database import Base


class Promo(Base):
    __tablename__ = "promos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False)
    description = Column(String(200))
    discount_type = Column(String(20), nullable=False)  # e.g., 'Percentage', 'Fixed Amount'
    value = Column(DECIMAL(5, 2), nullable=False)

    start_date = Column(DATETIME)
    end_date = Column(DATETIME)
    is_active = Column(Integer, default=1)  # Boolean equivalent