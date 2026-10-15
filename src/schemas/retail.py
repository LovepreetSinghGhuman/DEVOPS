from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransactionCreate(BaseModel):
    invoice_no: str
    stock_code: str
    description: Optional[str] = None
    quantity: int
    unit_price: float
    customer_id: Optional[str] = None
    country: Optional[str] = None

class TransactionResponse(BaseModel):
    id: int
    invoice_no: str
    stock_code: str
    description: Optional[str] = None
    quantity: int
    unit_price: float
    total_amount: float
    customer_id: Optional[str] = None
    country: Optional[str] = None
    is_fraudulent: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SalesSummaryResponse(BaseModel):
    total_transactions: int
    total_revenue: float
    fraudulent_count: int
    cached: bool
