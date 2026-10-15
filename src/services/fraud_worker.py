import time
from src.core.celery_app import celery_app
from src.core.database import SessionLocal
from src.models.retail import TransactionModel

@celery_app.task(name="scan_transaction_fraud")
def scan_transaction_fraud(transaction_id: int):
    print(f"Starting background fraud scan for Transaction ID: {transaction_id}")
    # Simulate machine learning inference delay (e.g., autoencoder anomaly threshold check)
    time.sleep(2)
    
    db = SessionLocal()
    try:
        tx = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
        if not tx:
            print(f"Transaction {transaction_id} not found.")
            return

        # Simple rule-based ML surrogate heuristic: High quantity or unit price marks fraud
        is_fraud = tx.total_amount > 10000 or tx.quantity > 200
        tx.is_fraudulent = is_fraud
        db.commit()
        print(f"Fraud scan complete for TX {transaction_id}. Marked fraudulent: {is_fraud}")
    finally:
        db.close()
