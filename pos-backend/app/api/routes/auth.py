import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.user import UserCreate
from app.schemas.auth import LoginRequest
from app.models.user import User
from app.models.refresh_token import RefreshToken
from datetime import datetime, timedelta
from app.core.security import verify_password
from app.core.security import create_access_token, create_refresh_token
from app.utils.id_generator import generate_user_id

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    user_id = generate_user_id(db)

    db_user = User(
        id=user_id,
        name=user.name,
        phone=user.phone,
        password=hash_password(user.password),
        role=user.role,
        dob=user.dob,
        designation=user.designation,
        location=user.location
    )

    db.add(db_user)
    db.commit()

    return {"user_id": user_id}


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == data.phone).first()

    if not user:
        return {"error": "User not found"}

    if not verify_password(data.password, user.password):
        return {"error": "Invalid password"}

    access_token = create_access_token({
        "user_id": user.id,
        "role": user.role
    })

    refresh_token = create_refresh_token()

    db_token = RefreshToken(
        id=str(uuid.uuid4()),
        user_id=user.id,
        token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )

    db.add(db_token)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }



@router.post("/refresh")
def refresh_token(token: str, db: Session = Depends(get_db)):
    # 🔍 Find refresh token in DB
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == token
    ).first()

    if not db_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # ⏳ Check expiry
    if db_token.expires_at < datetime.utcnow():
        db.delete(db_token)
        db.commit()
        raise HTTPException(status_code=401, detail="Refresh token expired")

    # 🔍 Get user (IMPORTANT for role)
    user = db.query(User).filter(User.id == db_token.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 🔄 ROTATION: delete old refresh token
    db.delete(db_token)

    # 🔁 Create new refresh token
    new_refresh = create_refresh_token()

    new_db_token = RefreshToken(
        id=str(uuid.uuid4()),
        user_id=user.id,
        token=new_refresh,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )

    db.add(new_db_token)

    # 🔐 Create new access token (WITH ROLE ✅)
    new_access = create_access_token({
        "user_id": user.id,
        "role": user.role
    })

    db.commit()

    return {
        "access_token": new_access,
        "refresh_token": new_refresh
    }



@router.post("/logout")
def logout(token: str, db: Session = Depends(get_db)):
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == token
    ).first()

    if db_token:
        db.delete(db_token)
        db.commit()

    return {"message": "Logged out successfully"}
