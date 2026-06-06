from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    email: str
    password: str
    role: str

class VendorCreate(BaseModel):
    name: str
    category: Optional[str] = None
    gst_number: Optional[str] = None
    phone: Optional[str] = None
    contact_email: Optional[str] = None
    address: Optional[str] = None

class VendorOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class RFQCreate(BaseModel):
    title: str
    description: Optional[str] = None
    vendor_id: Optional[int] = None
    deadline: Optional[str] = None
    attachment_url: Optional[str] = None
