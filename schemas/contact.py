from pydantic import BaseModel, EmailStr


class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str


class ContactResponse(ContactCreate):
    id: int

    model_config = {
        "from_attributes": True
    }
