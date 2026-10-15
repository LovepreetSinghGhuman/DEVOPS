import json
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import jwt
import redis

from src.core.database import get_db, engine, Base
from src.core.cache import get_redis
from src.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    SECRET_KEY,
    ALGORITHM
)
from src.models.retail import TransactionModel
from src.models.user import UserModel
from src.schemas.retail import (
    TransactionResponse,
    SalesSummaryResponse,
    TransactionCreate
)
from src.schemas.user import UserCreate, UserResponse, Token
from src.services.fraud_worker import scan_transaction_fraud
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="RetailPulse API",
    description="High-performance retail sales analytics & fraud detection backend",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

Instrumentator().instrument(app).expose(app)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if user is None:
        raise credentials_exception
    return user

@app.get("/")
def read_root():
    return {"message": "Welcome to RetailPulse API! Head to /docs for interactive API documentation."}

@app.get("/transactions", response_model=list[TransactionResponse])
def get_transactions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    transactions = db.query(TransactionModel).offset(skip).limit(limit).all()
    return transactions

@app.post("/register", response_model=UserResponse, status_code=201)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = UserModel(
        email=payload.email,
        hashed_password=hash_password(payload.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password", headers={"WWW-Authenticate": "Bearer"})
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/transactions", response_model=TransactionResponse, status_code=201)
def create_transaction(
    payload: TransactionCreate, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user) # Requires valid JWT token!
):
    total_amt = payload.quantity * payload.unit_price
    new_tx = TransactionModel(
        invoice_no=payload.invoice_no,
        stock_code=payload.stock_code,
        description=payload.description,
        quantity=payload.quantity,
        unit_price=payload.unit_price,
        total_amount=total_amt,
        customer_id=payload.customer_id,
        country=payload.country,
        is_fraudulent=False
    )
    db.add(new_tx)
    db.commit()
    db.refresh(new_tx)

    # Asynchronously queue background fraud scan task
    scan_transaction_fraud.delay(new_tx.id)
    return new_tx

@app.get("/analytics/summary", response_model=SalesSummaryResponse)
def get_sales_summary(db: Session = Depends(get_db), r: redis.Redis = Depends(get_redis)):
    cache_key = "analytics:sales_summary"
    
    # 1. Try reading from Redis Cache (Cache-Aside pattern)
    cached_data = r.get(cache_key)
    if cached_data:
        data = json.loads(cached_data)
        data["cached"] = True
        return data

    # 2. Cache Miss: Compute from PostgreSQL Database
    total_tx = db.query(TransactionModel).count()
    if total_tx == 0:
        raise HTTPException(status_code=404, detail="No transaction data found")
    
    total_revenue = sum(tx.total_amount for tx in db.query(TransactionModel).all())
    fraud_count = db.query(TransactionModel).filter(TransactionModel.is_fraudulent == True).count()

    summary = {
        "total_transactions": total_tx,
        "total_revenue": round(total_revenue, 2),
        "fraudulent_count": fraud_count
    }

    # 3. Save result into Redis with a 60-second TTL
    r.setex(cache_key, 60, json.dumps(summary))

    summary["cached"] = False
    return summary
