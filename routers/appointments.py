from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.appointment import DbAppointment
from models.doctor import DbDoctor
from schemas.appointment import AppointmentCreate, Appointment, AppointmentWithDoctor
from utils.token_utils import get_current_user
from routers.auth import oauth2_scheme
from utils.email_utils import send_appointment_confirmation

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


@router.post("/", response_model=Appointment)
async def create_appointment(
    request: AppointmentCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    try:
        # Get current user
        current_user = await get_current_user(token, db)

        # Check if doctor exists
        doctor = db.query(DbDoctor).filter(
            DbDoctor.id == request.doctor_id).first()
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Doctor with id {request.doctor_id} not found"
            )

        # Check if doctor is available
        if not doctor.available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Doctor with id {request.doctor_id} is not available for appointments"
            )

        # Create new appointment
        new_appointment = DbAppointment(
            user_id=current_user.id,
            doctor_id=request.doctor_id,
            date_time=request.date_time
        )

        db.add(new_appointment)
        db.commit()
        db.refresh(new_appointment)

        # Get doctor details for email
        doctor = db.query(DbDoctor).filter(
            DbDoctor.id == request.doctor_id).first()
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found"
            )

    
        doctor_details = {
            "speciality": doctor.speciality['title'],
            "address": doctor.address['line1']
        }
        

        # Send confirmation email
        if send_appointment_confirmation(
            user_email=current_user.email,
            user_name=current_user.name,
            doctor_name=doctor.name,
            date_time=request.date_time,
            doctor_details=doctor_details
        ):
            print("Email sent successfully")
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send email"
            )

        return new_appointment

    except Exception as e:
        # Rollback the transaction in case of error
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create appointment: {str(e)}"
        )


@router.get("", response_model=List[AppointmentWithDoctor])
async def get_user_appointments(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    try:
        # Get current user
        current_user = await get_current_user(token, db)

        # Get appointments with complete doctor details
        appointments = db.query(DbAppointment).filter(
            DbAppointment.user_id == current_user.id
        ).all()

        if not appointments:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No appointments found for the user"
            )

        result = []
        for appt in appointments:
            try:
                # Get doctor details
                doctor = db.query(DbDoctor).filter(
                    DbDoctor.id == appt.doctor_id).first()
                if doctor:
                    result.append(
                        AppointmentWithDoctor(
                            id=appt.id,
                            date_time=appt.date_time,
                            doctor=doctor
                        )
                    )
            except Exception as inner_error:
                # Log the error but continue processing other appointments
                print(
                    f"Error processing appointment {appt.id}: {str(inner_error)}")
                continue

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No valid appointments found with doctor details"
            )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch appointments: {str(e)}"
        )
