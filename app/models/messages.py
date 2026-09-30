from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey, Text, func
)
from sqlalchemy.orm import declarative_base, relationship
from app.models.base import Base

class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True, autoincrement=True)
    topic_id = Column(Integer, ForeignKey("topics.topic_id"), nullable=False, index=True)
    is_user = Column(Boolean, nullable=False)  # True = from user, False = from bot
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
