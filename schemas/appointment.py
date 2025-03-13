from pydantic import BaseModel
from datetime import datetime


class AppointmentBase(BaseModel):
    doctor_id: int
    date_time: datetime

    model_config = {
        "from_attributes": True
    }


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentDetail(BaseModel):
    doctor_name: str
    speciality: str
    address: str
    date_time: datetime
    image: str

    model_config = {
        "from_attributes": True
    }


class Appointment(AppointmentBase):
    id: int
    user_id: int

    model_config = {
        "from_attributes": True
    }
