from pydantic import BaseModel, Field
from typing import Optional, List


class AddressSchema(BaseModel):
    line1: str
    line2: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class SpecialitySchema(BaseModel):
    title: str
    icon: str

    model_config = {
        "from_attributes": True
    }


class DepartmentResponse(BaseModel):
    departments: List[SpecialitySchema]

    model_config = {
        "from_attributes": True
    }


class DoctorCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    about: Optional[str] = Field(None, max_length=500)
    address: AddressSchema
    degree: str = Field(..., min_length=2, max_length=50)
    experience: str = Field(..., min_length=2, max_length=20)
    fees: int = Field(..., gt=0)
    image: Optional[str] = None
    speciality: SpecialitySchema
    available: bool = True


class DoctorResponse(BaseModel):
    id: int
    name: str
    about: str
    address: AddressSchema
    degree: str
    experience: str
    fees: int
    image: str
    speciality: SpecialitySchema
    available: bool

    model_config = {
        "from_attributes": True
    }
