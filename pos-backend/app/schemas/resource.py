from pydantic import BaseModel
from typing import Optional


class ResourceCreate(BaseModel):
    name: str
    resource_type: str
    description: Optional[str] = None
    price: float
    instock_quantity: int
    resource_location: str
    image_url: Optional[str] = None


class ResourceResponse(BaseModel):
    id: str
    name: str
    resource_type: str
    price: float
    instock_quantity: int

    class Config:
        from_attributes = True
