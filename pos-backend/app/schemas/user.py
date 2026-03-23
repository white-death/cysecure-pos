from pydantic import BaseModel
from datetime import date

class UserCreate(BaseModel):
    name: str
    phone: str
    password: str
    role: str
    dob: date
    designation: str
    location: str
