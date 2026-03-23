from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import hash_password, create_token
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
def login(phone: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == phone).first()

    if not user:
        return {"error": "User not found"}

    from app.core.security import verify_password

    if not verify_password(password, user.password):
        return {"error": "Invalid password"}

    token = create_token({
        "user_id": user.id,
        "role": user.role
    })

    return {"access_token": token}
