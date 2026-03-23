from datetime import datetime
from sqlalchemy.orm import Session
from app.models.user import User

def generate_user_id(db: Session):
    year = datetime.now().year

    prefix = f"ENXU{year}"

    last_user = (
        db.query(User)
        .filter(User.id.like(f"{prefix}%"))
        .order_by(User.id.desc())
        .first()
    )

    if last_user:
        last_number = int(last_user.id[-6:])
        new_number = last_number + 1
    else:
        new_number = 1

    return f"{prefix}{str(new_number).zfill(6)}"
