from sqlalchemy import (
    Column,
    String,
    Integer,
    Numeric,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.db.base import Base


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    invoice_id = Column(
        String,
        ForeignKey("invoices.id")
    )

    resource_id = Column(
        String,
        ForeignKey("resources.id")
    )

    item_name = Column(String)

    item_type = Column(String)

    quantity = Column(Integer)

    unit_price = Column(
        Numeric(10, 2)
    )

    total_price = Column(
        Numeric(10, 2)
    )

    invoice = relationship(
        "Invoice",
        back_populates="items"
    )
