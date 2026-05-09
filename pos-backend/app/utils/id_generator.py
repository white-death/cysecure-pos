from datetime import datetime
from sqlalchemy.orm import Session
from app.models.user import User


PREFIX_MAP = {
    "food": "FD",
    "beverage": "BV",
    "dessert": "DS",
    "sellable": "SL",
    "merchandise": "MH"
}

def generate_enxu_id(db: Session):
    year = datetime.now().year

    count = db.query(User).count() + 1

    serial = str(count).zfill(6)

    return f"ENXU{year}{serial}"


def generate_resource_id(resource_type: str, serial: int):
    year = datetime.utcnow().year

    type_code = PREFIX_MAP[resource_type.lower()]

    return f"EX{type_code}{year}{serial:04d}"
