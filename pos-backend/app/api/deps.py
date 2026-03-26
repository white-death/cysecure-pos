from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.core.oidc import verify_token
from app.db.session import SessionLocal
from app.models.user import User

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials=Depends(security),
    db: Session = Depends(get_db)
):
    payload = verify_token(credentials.credentials)

    keycloak_id = payload.get("sub")

    user = db.query(User).filter(
        User.keycloak_id == keycloak_id
    ).first()

    if not user:
        raise HTTPException(403, "User not registered by admin")

    return user


def require_admin(user=Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(403, "Admin only")
    return user
