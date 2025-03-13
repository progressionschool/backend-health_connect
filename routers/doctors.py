from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import DbDoctor
from schemas.doctor import DoctorCreate, DoctorResponse, DepartmentResponse, SpecialitySchema
from routers.auth import oauth2_scheme
from typing import List


router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)


@router.get("/deptt/{deptt_name}", response_model=List[DoctorResponse])
async def get_doctors_by_department(
    deptt_name: str,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    try:
        # First, let's get all doctors to see what we have
        all_doctors = db.query(DbDoctor).all()

        # Filter doctors based on speciality title
        matching_doctors = []
        for doctor in all_doctors:
            if doctor.speciality and "title" in doctor.speciality:
                if doctor.speciality["title"].lower() == deptt_name.lower():
                    matching_doctors.append(doctor)

        if not matching_doctors:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No doctors found in department: {deptt_name}"
            )

        return matching_doctors
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch doctors: {str(e)}"
        )


@router.get("/deptt", response_model=DepartmentResponse)
async def get_departments(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    try:
        # Get all doctors and extract unique specialities
        doctors = db.query(DbDoctor).all()

        # Create a set to store unique departments (using tuple of title and icon)
        unique_departments = set()
        for doctor in doctors:
            speciality = doctor.speciality
            unique_departments.add((speciality["title"], speciality["icon"]))

        # Convert to list of SpecialitySchema
        departments = [
            SpecialitySchema(title=title, icon=icon)
            for title, icon in sorted(unique_departments)
        ]

        return {"departments": departments}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch departments: {str(e)}"
        )


@router.get("/{doctor_id}", response_model=DoctorResponse)
async def get_doctor_by_id(
    doctor_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    try:
        doctor = db.query(DbDoctor).filter(DbDoctor.id == doctor_id).first()
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Doctor with id {doctor_id} not found"
            )
        return doctor
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch doctor: {str(e)}"
        )


@router.get("", response_model=List[DoctorResponse])
async def get_all_doctors(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    try:
        doctors = db.query(DbDoctor).all()
        return doctors
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch doctors: {str(e)}"
        )


@router.post("", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
async def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    try:
        # Convert the Pydantic model to SQLAlchemy model
        db_doctor = DbDoctor(
            name=doctor.name,
            about=doctor.about,
            address=doctor.address.model_dump(),
            degree=doctor.degree,
            experience=doctor.experience,
            fees=doctor.fees,
            image=doctor.image,
            speciality=doctor.speciality.model_dump(),
            available=doctor.available
        )

        # Add to database
        db.add(db_doctor)
        db.commit()
        db.refresh(db_doctor)

        return db_doctor

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create doctor: {str(e)}"
        )
