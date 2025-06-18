from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class ContactBase(BaseModel):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    email: EmailStr
    phone: Optional[str] = None
    notes: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    notes: Optional[str] = None

class ContactOut(ContactBase):
    id: int

    class Config:
        orm_mode = True 