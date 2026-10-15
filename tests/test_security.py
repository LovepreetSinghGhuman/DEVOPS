from src.core.security import hash_password, verify_password


def test_hash_and_verify_password():
    password = "password123"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
