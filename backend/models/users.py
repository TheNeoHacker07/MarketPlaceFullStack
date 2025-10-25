from sqlalchemy import Integer, Text, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base

class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    user_products = relationship("Product", back_populates="user")
    user_cart = relationship("Cart", back_populates="user")
    user_order = relationship("Order", back_populates="user")

    def __str__(self):
        return self.email
