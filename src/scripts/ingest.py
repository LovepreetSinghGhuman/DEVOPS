import pandas as pd
from src.core.database import engine, Base
from src.models.retail import TransactionModel
from sqlalchemy.orm import Session

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

def load_sample_data():
    session = Session(engine)
    
    # Check if data already exists
    if session.query(TransactionModel).count() > 0:
        print("Data already loaded. Skipping ingestion.")
        session.close()
        return

    print("Generating and inserting sample retail records...")
    # Creating sample rows reflecting public dataset schema structures
    sample_data = [
        {
            "invoice_no": "INV-54321",
            "stock_code": "85123A",
            "description": "WHITE HANGING HEART T-LIGHT HOLDER",
            "quantity": 6,
            "unit_price": 2.55,
            "total_amount": 15.30,
            "customer_id": "CUST-1001",
            "country": "United Kingdom",
            "is_fraudulent": False
        },
        {
            "invoice_no": "INV-54322",
            "stock_code": "71053",
            "description": "WHITE METAL LANTERN",
            "quantity": 12,
            "unit_price": 3.39,
            "total_amount": 40.68,
            "customer_id": "CUST-1002",
            "country": "France",
            "is_fraudulent": False
        },
        {
            "invoice_no": "INV-99999",
            "stock_code": "FLAG-99",
            "description": "HIGH-VALUE SUSPICIOUS ITEM",
            "quantity": 500,
            "unit_price": 999.99,
            "total_amount": 499995.00,
            "customer_id": "CUST-9999",
            "country": "Unknown",
            "is_fraudulent": True  # Seeded for fraud detector validation
        }
    ]

    for item in sample_data:
        db_item = TransactionModel(**item)
        session.add(db_item)
    
    session.commit()
    session.close()
    print("Sample retail data successfully loaded into PostgreSQL!")

if __name__ == "__main__":
    init_db()
    load_sample_data()
