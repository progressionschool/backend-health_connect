from pydantic import BaseModel, EmailStr
from typing import List
from schemas.appointment import AppointmentDetail


class UserBase(BaseModel):
    name: str
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class User(UserBase):
    id: int

    model_config = {
        "from_attributes": True
    }


class UserWithAppointments(User):
    appointments: List[AppointmentDetail] = []

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True
    }
