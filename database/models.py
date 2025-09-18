from datetime import datetime

from database.settings import Base, engine
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Time, Date, DateTime

class Person(Base):
    __tablename__ = "Person"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    age = Column(Integer)
    phone = Column(String, unique=True)
    email = Column(String, unique=True)
    address = Column(String)
    health_status = Column(String)
    shelter_status = Column(String)
    patients = Column(Integer)
    needs = Column(String)
    status = Column(String, default="PROCESSING")
    score = Column(Integer)
    explanation = Column(String)
    date_created = Column(DateTime, default=datetime.now)
