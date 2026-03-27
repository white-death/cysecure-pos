from sqlalchemy import Column, String, Integer, Date

from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)  # ENXU ID
    keycloak_id = Column(String)

    first_name = Column(String)
    last_name = Column(String)
    dob = Column(Date)

    designation = Column(String)
    role = Column(String)

    phone = Column(String, unique=True)
    location = Column(String)

    rating = Column(Integer, default=0)  # ⭐ out of 5
