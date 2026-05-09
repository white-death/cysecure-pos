from pydantic import BaseModel
from typing import List, Optional


class InvoiceItemCreate(BaseModel):

    resource_id: str

    item_name: str

    item_type: str

    quantity: int

    unit_price: float

    total_price: float


class InvoiceCreate(BaseModel):

    customer_id: Optional[str] = None

    cashier_id: str

    customer_phone_number: Optional[str] = None

    customer_email_address: Optional[str] = None

    items: List[InvoiceItemCreate]

    edible_total: float = 0

    sellable_total: float = 0

    loyalty_points_used: int = 0

    edible_discount: float = 0

    sellable_discount: float = 0

    invoice_discount: float = 0

    manual_discount: float = 0

    gst_charge: float = 0

    outlet_charge: float = 0

    order_type: str

    grand_total: float

    payment_method: str

    txn_receipt: Optional[str] = None

    store_id: str

    store_name: str

    store_location: str

    table_number: Optional[str] = None

    receipt_path: Optional[str] = None
