from pydantic import BaseModel, Field
from datetime import datetime



class RegistrationInfoSchema(BaseModel):
    username: str = Field(..., max_length=50)
    email_or_phone: str = Field(..., max_length=255)
    password: str = Field(...)



class LoginInfoSchema(BaseModel):
    email_or_phone: str
    password: str


class UserResponseSchema(BaseModel):
    user_id: int
    username: str
    email_or_phone: str
    


class TopicCreate(BaseModel):
    topic: str
    user_id: int

class TopicsFetch(BaseModel):
    user_id: int

class TopicOut(BaseModel):
    topic_id: int
    topic: str
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    topic_id: int
    is_user: bool
    content: str


class MessageOut(BaseModel):
    message_id: int
    topic_id: int
    is_user: bool
    content: str
    created_at: datetime

    class Config:
        from_attributes = True



class GoogleLoginRequest(BaseModel):
    id_token: str