from sqlalchemy import (
    Column,
    String,
    Integer,
    Numeric,
    Boolean,
    DateTime
)

from datetime import datetime

from app.db.base import Base


class Resource(Base):
    __tablename__ = "resources"

    id = Column(String, primary_key=True)

    name = Column(String, nullable=False)

    resource_type = Column(String, nullable=False)

    description = Column(String)

    price = Column(Numeric(10, 2), nullable=False)

    instock_quantity = Column(Integer, default=0)

    resource_location = Column(String)

    image_url = Column(String)

    barcode = Column(String, unique=True)

    sku = Column(String, unique=True)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(DateTime, default=datetime.utcnow)
