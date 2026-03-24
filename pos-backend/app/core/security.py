from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------------- Password Hashing ----------------
def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


# ---------------- JWT Token ----------------
def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=12)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
