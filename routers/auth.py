from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from database import get_db
from models import DbUser
from schemas.user import UserCreate
from schemas.token import Token
from utils.password_utils import get_password_hash, verify_password
from utils.email_utils import generate_otp, send_verification_email
from utils.token_utils import create_access_token
from config import settings
from pydantic import BaseModel
from typing import Dict

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Temporary storage for unverified users
unverified_users: Dict[str, dict] = {}


class VerifyEmail(BaseModel):
    email: str
    verification_code: str


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username exists in verified users
    if db.query(DbUser).filter(DbUser.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Check if email exists in verified users
    if db.query(DbUser).filter(DbUser.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Check if email exists in unverified users
    if user.email in unverified_users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered but not verified. Please check your email for verification code."
        )

    # Generate OTP
    otp = generate_otp()

    # Store user data temporarily
    unverified_users[user.email] = {
        "name": user.name,
        "username": user.username,
        "email": user.email,
        "password": user.password,
        "verification_code": otp
    }

    # Send verification email
    email_sent = send_verification_email(user.email, otp)
    if not email_sent:
        # Remove from unverified users if email sending fails
        unverified_users.pop(user.email, None)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send verification email"
        )

    return {"message": "Signup successful. Please check your email for verification code."}


@router.post("/verify-email", status_code=status.HTTP_200_OK)
async def verify_email(verify_data: VerifyEmail, db: Session = Depends(get_db)):
    # Check if email exists in unverified users
    if verify_data.email not in unverified_users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found or already verified"
        )

    user_data = unverified_users[verify_data.email]

    if user_data["verification_code"] != verify_data.verification_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code"
        )

    # Create verified user in database
    db_user = DbUser(
        name=user_data["name"],
        username=user_data["username"],
        email=user_data["email"],
        hashed_password=get_password_hash(user_data["password"]),
        is_verified=True
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Remove from unverified users after successful verification
    unverified_users.pop(verify_data.email)

    return {"message": "Email verified successfully"}


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please verify your email first"
        )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
