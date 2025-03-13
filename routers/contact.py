from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import DbContact
from schemas.contact import ContactCreate, ContactResponse
from typing import List

router = APIRouter(
    prefix="/contact",
    tags=["Contact"]
)


@router.post("/get_in_touch", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    contact: ContactCreate,
    db: Session = Depends(get_db)
):
    try:
        # Convert the Pydantic model to SQLAlchemy model
        db_contact = DbContact(
            name=contact.name,
            email=contact.email,
            subject=contact.subject,
            message=contact.message
        )

        # Add to database
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)

        return db_contact

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save message: {str(e)}"
        )


@router.get("/messages", response_model=List[ContactResponse])
async def get_all_messages(db: Session = Depends(get_db)):
    try:
        messages = db.query(DbContact).all()
        return messages
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch messages: {str(e)}"
        )
