from sqlalchemy import (
    Column,
    String,
    Integer,
    Numeric,
    DateTime,
    ForeignKey
)

from datetime import datetime

from sqlalchemy.orm import relationship

from app.db.base import Base


class Invoice(Base):
    __tablename__ = "invoices"

    # ENXI2026000001
    id = Column(String, primary_key=True)

    customer_id = Column(
        String,
        ForeignKey("customers.id"),
        nullable=True
    )

    # ENXU User ID
    cashier_id = Column(
        String,
        ForeignKey("users.id"),
        nullable=False
    )

    customer_phone_number = Column(
        String,
        nullable=True
    )

    customer_email_address = Column(
        String,
        nullable=True
    )

    edible_total = Column(
        Numeric(10, 2),
        default=0
    )

    sellable_total = Column(
        Numeric(10, 2),
        default=0
    )

    loyalty_points_used = Column(
        Integer,
        default=0
    )

    edible_discount = Column(
        Numeric(10, 2),
        default=0
    )

    sellable_discount = Column(
        Numeric(10, 2),
        default=0
    )

    invoice_discount = Column(
        Numeric(10, 2),
        default=0
    )

    manual_discount = Column(
        Numeric(10, 2),
        default=0
    )

    gst_charge = Column(
        Numeric(10, 2),
        default=0
    )

    outlet_charge = Column(
        Numeric(10, 2),
        default=0
    )

    order_type = Column(String)

    grand_total = Column(
        Numeric(10, 2),
        nullable=False
    )

    payment_method = Column(String)

    txn_receipt = Column(String)

    store_id = Column(String)

    store_name = Column(String)

    store_location = Column(String)

    table_number = Column(String)

    invoice_date_and_time = Column(
        DateTime,
        default=datetime.utcnow
    )

    receipt_path = Column(String)

    items = relationship(
        "InvoiceItem",
        back_populates="invoice",
        cascade="all, delete"
    )
