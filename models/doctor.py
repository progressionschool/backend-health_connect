from sqlalchemy import Column, Integer, String, Boolean, JSON
from database import Base


class DbDoctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    about = Column(String, nullable=True)
    address = Column(JSON, nullable=False)
    available = Column(Boolean, default=True)
    degree = Column(String, nullable=False)
    experience = Column(String, nullable=False)
    fees = Column(Integer, nullable=False)
    image = Column(String, nullable=True)
    speciality = Column(JSON, nullable=False)
