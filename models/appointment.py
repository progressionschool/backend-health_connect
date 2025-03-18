from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class DbAppointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    date_time = Column(String)

    # Relationships
    user = relationship("DbUser", back_populates="appointments")
    doctor = relationship("DbDoctor", back_populates="appointments")
