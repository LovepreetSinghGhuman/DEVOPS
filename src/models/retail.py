from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.core.database import Base

class TransactionModel(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    invoice_no = Column(String, index=True)
    stock_code = Column(String, index=True)
    description = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    customer_id = Column(String, index=True, nullable=True)
    country = Column(String, nullable=True)
    is_fraudulent = Column(Boolean, default=False)  # Target flag for our ML fraud worker later!
    created_at = Column(DateTime(timezone=True), server_default=func.now())
