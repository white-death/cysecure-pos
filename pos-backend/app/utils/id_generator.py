from datetime import datetime
from sqlalchemy.orm import Session
from app.models.user import User

def generate_enxu_id(db: Session):
    year = datetime.now().year

    count = db.query(User).count() + 1

    serial = str(count).zfill(6)

    return f"ENXU{year}{serial}"
