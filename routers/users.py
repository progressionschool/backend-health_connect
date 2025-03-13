from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import DbUser, DbDoctor
from schemas.user import UserWithAppointments
from schemas.appointment import AppointmentDetail
from routers.auth import oauth2_scheme


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/{user_id}", response_model=UserWithAppointments)
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    try:
        # Get user with appointments
        user = db.query(DbUser).filter(DbUser.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )

        # Get appointments with doctor details
        appointments = []
        for appt in user.appointments:
            doctor = db.query(DbDoctor).filter(
                DbDoctor.id == appt.doctor_id).first()
            if doctor:
                # Format address
                address_dict = doctor.address
                address = f"{address_dict['line1']}, {address_dict['line2']}" if address_dict['line2'] else address_dict['line1']

                # Create appointment detail
                appointment_detail = AppointmentDetail(
                    doctor_name=doctor.name,
                    speciality=doctor.speciality["title"],
                    address=address,
                    date_time=appt.date_time,
                    image=doctor.image
                )
                appointments.append(appointment_detail)

        # Create response
        response = UserWithAppointments(
            id=user.id,
            name=user.name,
            username=user.username,
            email=user.email,
            appointments=appointments
        )

        return response

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch user: {str(e)}"
        )
