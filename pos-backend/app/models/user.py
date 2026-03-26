from sqlalchemy import Column, String, Date
from app.db.base import Base
from datetime import date

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)  # ENXU2026000001
    keycloak_id = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)

    role = Column(String, nullable=False)  # admin, cashier, manager

    dob = Column(Date)
    designation = Column(String)
    location = Column(String)
