from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.repositories.topics_repository import TopicsRepository
from app.repositories.messages_repository import MessagesRepository
from app.data_schemas import TopicCreate, TopicsFetch, TopicOut, MessageCreate, MessageOut
from typing import List

router = APIRouter()


@router.post("/create_topic", response_model=TopicOut)
async def create_topic(payload: TopicCreate):
    record = await TopicsRepository.create_topic(
        topic=payload.topic,
        user_id=payload.user_id,
    )
    if record is None:
        raise HTTPException(status_code=400, detail="Failed to create topic")
    return TopicOut(**dict(record))

@router.post("/get_topics", response_model=List[TopicOut])
async def get_topics(payload: TopicsFetch):
    records = await TopicsRepository.get_topics_by_user(
        user_id= payload.user_id
    )
    
    if records is None:
        raise HTTPException(status_code=400, detail="Failed to create topic")
    
    return [TopicOut(**dict(r)) for r in records]


# @router.get("/topics/{topic_id}", response_model=TopicOut)
# async def get_topic(topic_id: int):
#     record = await TopicsRepository.get_topic_by_id(topic_id)
#     if record is None:
#         raise HTTPException(status_code=404, detail="Topic not found")
#     return TopicOut(**dict(record))


# @router.get("/topics/user/{user_id}", response_model=list[TopicOut])
# async def get_topics_for_user(user_id: int):
#     records = await TopicsRepository.get_topics_by_user(user_id)
#     return [TopicOut(**dict(r)) for r in records]


# @router.delete("/topics/{topic_id}")
# async def delete_topic(topic_id: int):
#     existing = await TopicsRepository.get_topic_by_id(topic_id)
#     if existing is None:
#         raise HTTPException(status_code=404, detail="Topic not found")
#     await TopicsRepository.delete_topic(topic_id)
#     return {"detail": "Topic deleted"}



@router.post("/create_message", response_model=MessageOut)
async def create_message(payload: MessageCreate):
    # Make sure the topic actually exists before attaching a message to it
    topic = await TopicsRepository.get_topic_by_id(payload.topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")

    record = await MessagesRepository.create_message(
        topic_id=payload.topic_id,
        is_user=payload.is_user,
        content=payload.content,
    )
    if record is None:
        raise HTTPException(status_code=400, detail="Failed to create message")
    return MessageOut(**dict(record))


@router.get("/messages/{topic_id}", response_model=list[MessageOut])
async def get_messages_for_topic(topic_id: int):
    records = await MessagesRepository.get_messages_by_topic(topic_id)
    return [MessageOut(**dict(r)) for r in records]