from pydantic import BaseModel
from typing import Optional
from datetime import date


class CustomerCreate(BaseModel):

    phone_number: Optional[str] = None

    email_address: Optional[str] = None

    first_name: Optional[str] = None

    last_name: Optional[str] = None

    special_occasion_date: Optional[date] = None

    special_occasion_description: Optional[str] = None

    feedback_recommendations: Optional[str] = None

    frequent_order_type: Optional[str] = None

    crypto_wallet_address: Optional[str] = None


class CustomerResponse(BaseModel):

    id: str

    phone_number: Optional[str]

    email_address: Optional[str]

    first_name: Optional[str]

    last_name: Optional[str]

    loyalty_points: int

    loyalty_progress: str

    class Config:
        from_attributes = True
