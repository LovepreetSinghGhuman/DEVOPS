from fastapi.testclient import TestClient
from src.main import app
from src.core.database import engine, Base
from src.models.retail import TransactionModel
from src.models.user import UserModel

def test_read_root():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert "Welcome" in response.json()["message"]

def test_register_and_login():
    # Ensure tables are created in the test database
    Base.metadata.create_all(bind=engine)
    
    test_email = "ci_tester@retailpulse.com"
    test_password = "password123"

    with TestClient(app) as client:
        # 1. Register User
        response = client.post("/register", json={"email": test_email, "password": test_password})
        assert response.status_code in [201, 400]

        # 2. Login to get JWT Token
        login_response = client.post(
            "/token",
            data={"username": test_email, "password": test_password}
        )
        assert login_response.status_code == 200
        data = login_response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
