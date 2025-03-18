from pydantic import BaseModel
from typing import Optional
from schemas.doctor import DoctorResponse


class AppointmentBase(BaseModel):
    doctor_id: int
    date_time: str

    model_config = {
        "from_attributes": True
    }


class AppointmentCreate(AppointmentBase):
    pass


class Appointment(BaseModel):
    id: int
    user_id: int
    doctor_id: int
    date_time: str

    model_config = {
        "from_attributes": True
    }


class AppointmentDetail(BaseModel):
    doctor_name: str
    speciality: str
    address: str
    date_time: str
    image: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class AppointmentWithDoctor(BaseModel):
    id: int
    date_time: str
    doctor: DoctorResponse

    model_config = {
        "from_attributes": True
    }
