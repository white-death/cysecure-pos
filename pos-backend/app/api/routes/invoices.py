from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.session import SessionLocal

from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem

from app.schemas.invoice import InvoiceCreate

from app.utils.id_generator import (
    generate_invoice_id
)

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)


# DATABASE SESSION
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE INVOICE
@router.post("/")
def create_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db)
):

    # GENERATE INVOICE ID
    count = db.query(Invoice).count()

    invoice_id = generate_invoice_id(
        count + 1
    )

    # CREATE MAIN INVOICE
    new_invoice = Invoice(

        id=invoice_id,

        customer_id=invoice.customer_id,

        cashier_id=invoice.cashier_id,

        customer_phone_number=invoice.customer_phone_number,

        customer_email_address=invoice.customer_email_address,

        edible_total=invoice.edible_total,

        sellable_total=invoice.sellable_total,

        loyalty_points_used=invoice.loyalty_points_used,

        edible_discount=invoice.edible_discount,

        sellable_discount=invoice.sellable_discount,

        invoice_discount=invoice.invoice_discount,

        manual_discount=invoice.manual_discount,

        gst_charge=invoice.gst_charge,

        outlet_charge=invoice.outlet_charge,

        order_type=invoice.order_type,

        grand_total=invoice.grand_total,

        payment_method=invoice.payment_method,

        txn_receipt=invoice.txn_receipt,

        store_id=invoice.store_id,

        store_name=invoice.store_name,

        store_location=invoice.store_location,

        table_number=invoice.table_number,

        receipt_path=invoice.receipt_path
    )

    db.add(new_invoice)

    # ADD ITEMS
    for item in invoice.items:

        invoice_item = InvoiceItem(

            invoice_id=invoice_id,

            resource_id=item.resource_id,

            item_name=item.item_name,

            item_type=item.item_type,

            quantity=item.quantity,

            unit_price=item.unit_price,

            total_price=item.total_price
        )

        db.add(invoice_item)

    db.commit()

    return {
        "message": "Invoice created successfully",
        "invoice_id": invoice_id
    }
