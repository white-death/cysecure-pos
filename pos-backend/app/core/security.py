from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.core.config import settings
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------------- PASSWORD ----------------
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


# ---------------- ACCESS TOKEN ----------------
def create_access_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=15)
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")


# ---------------- REFRESH TOKEN ----------------
def create_refresh_token():
    return str(uuid.uuid4())
