from datetime import datetime

from database.settings import Base, engine
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Time, Date, DateTime

class Lesson(Base):
    __tablename__ = "Lesson"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    unit_count = Column(Integer, default=10)
    unit_1 = Column(String, nullable=True)
    unit_2 = Column(String, nullable=True)
    unit_3 = Column(String, nullable=True)
    unit_4 = Column(String, nullable=True)
    unit_5 = Column(String, nullable=True)
    unit_6 = Column(String, nullable=True)
    unit_7 = Column(String, nullable=True)
    unit_8 = Column(String, nullable=True)
    unit_9 = Column(String, nullable=True)
    unit_10 = Column(String, nullable=True)
    ring = Column(Integer, default=1)
    total_duration = Column(String, nullable=True)
    date_created = Column(DateTime, default=datetime.now)


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    adhd_type = Column(String, nullable=True)
    learning_style = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    date_joined = Column(DateTime, default=datetime.now)


class User_statistics(Base):
    __tablename__ = "User_statistics"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    daily_progress = Column(Integer, default=0)
    weekly_progress = Column(Integer, default=0)
    monthly_progress = Column(Integer, default=0)
    total_study_time = Column(String, default="00:00:00")
    completed_lessons = Column(Integer, default=0)
    completed_units = Column(Integer, default=0)
    completed_quizzes = Column(Integer, default=0)
    average_quiz_score = Column(Integer, default=0)
    focus_points = Column(Integer, default=0)
    last_activity = Column(DateTime, default=datetime.now)
    last_accessed = Column(DateTime, default=datetime.now)


class Chat_history(Base):
    __tablename__ = "Chat_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    message = Column(String, nullable=False)
    response = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)