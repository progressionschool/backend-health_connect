from routers.auth import router as auth_router
from routers.doctors import router as doctor_router
from routers.users import router as user_router
from routers.appointments import router as appointment_router

__all__ = ["auth_router", "doctor_router", "user_router", "appointment_router"]
