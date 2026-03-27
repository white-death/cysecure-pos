from pydantic import BaseModel
from datetime import date

class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    dob: date
    designation: str
    role: str
    phone: str
    location: str
