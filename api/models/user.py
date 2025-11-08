from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrememnt=True)

    name = Column(String(100), nullable=False)
    phone_number = Column(String(20))
    address = Column(String(255))

    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)

    role = Column(String(50), default="Customer")

    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")