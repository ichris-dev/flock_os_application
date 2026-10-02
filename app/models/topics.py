from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey, Text, func
)
from sqlalchemy.orm import declarative_base, relationship
from app.models.base import Base



class Topic(Base):
    __tablename__ = "topics"

    topic_id = Column(Integer, primary_key=True, autoincrement=True)
    topic = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)  # add ForeignKey("users.id") if you have a users table
    created_at = Column(DateTime, server_default=func.now())