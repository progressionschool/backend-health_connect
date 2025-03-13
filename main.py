from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers.auth import router as auth_router
from routers.doctors import router as doctor_router
from routers.users import router as user_router
from routers.contact import router as contact_router
from routers.appointments import router as appointment_router
from utils.seed_doctors import seed_doctors

app = FastAPI(
    title="Health Connect API",
    description="API for Health Connect application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Create tables
Base.metadata.create_all(bind=engine)

# Seed initial data
seed_doctors()

# Include routers
app.include_router(auth_router)
app.include_router(doctor_router)
app.include_router(user_router)
app.include_router(contact_router)
app.include_router(appointment_router)
