from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import DbAppointment, DbDoctor
from schemas.appointment import AppointmentCreate, Appointment
from routers.auth import oauth2_scheme
from utils.token_utils import get_current_user

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


@router.post("", response_model=Appointment, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    try:
        # Get the current user from the token
        current_user = await get_current_user(token, db)

        # Check if doctor exists and is available
        doctor = db.query(DbDoctor).filter(
            DbDoctor.id == appointment.doctor_id).first()
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Doctor with id {appointment.doctor_id} not found"
            )

        if not doctor.available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Doctor with id {appointment.doctor_id} is not available for appointments"
            )

        # Create appointment
        db_appointment = DbAppointment(
            user_id=current_user.id,
            doctor_id=appointment.doctor_id,
            date_time=appointment.date_time
        )

        # Add to database
        db.add(db_appointment)
        db.commit()
        db.refresh(db_appointment)

        return db_appointment

    except Exception as e:
        db.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create appointment: {str(e)}"
        )
