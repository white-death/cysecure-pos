from sqlalchemy import (
    Column,
    String,
    Integer,
    Numeric,
    Date,
    DateTime,
    JSON,
    Text
)

from datetime import datetime

from app.db.base import Base


class Customer(Base):
    __tablename__ = "customers"

    # ENXC2026000001
    id = Column(String, primary_key=True)

    phone_number = Column(
        String,
        unique=True,
        nullable=True
    )

    email_address = Column(
        String,
        unique=True,
        nullable=True
    )

    first_name = Column(
        String,
        nullable=True
    )

    last_name = Column(
        String,
        nullable=True
    )

    special_occasion_date = Column(
        Date,
        nullable=True
    )

    special_occasion_description = Column(
        String,
        nullable=True
    )

    last_visit_date = Column(
        DateTime,
        nullable=True
    )

    frequently_ordered_items = Column(
        JSON,
        nullable=True
    )

    feedback_recommendations = Column(
        Text,
        nullable=True
    )

    loyalty_points = Column(
        Integer,
        default=0
    )

    # Bronze / Silver / Gold / Platinum
    loyalty_progress = Column(
        String,
        default="Bronze"
    )

    last_bill_items = Column(
        JSON,
        nullable=True
    )

    last_bill_amount = Column(
        Numeric(10, 2),
        nullable=True
    )

    frequent_order_type = Column(
        String,
        nullable=True
    )

    crypto_wallet_address = Column(
        String,
        nullable=True
    )

    crypto_wallet_balance = Column(
        Numeric(18, 8),
        default=0
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow
    )
