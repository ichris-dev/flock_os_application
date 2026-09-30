import asyncpg
from app.db.db_connection import get_pool
from typing import List


class TopicsRepository:
    """Owns all SQL for the topics table. The API layer talks to this,
    never to asyncpg directly."""

    @staticmethod
    async def create_topic(topic: str, user_id: int) -> asyncpg.Record:
        query = """
            INSERT INTO topics (topic, user_id)
            VALUES ($1, $2)
            RETURNING topic_id, topic, user_id, created_at
        """
        pool = await get_pool()
        async with pool.acquire() as conn:
            return await conn.fetchrow(query, topic, user_id)
    

    @staticmethod
    async def get_topic_by_id(topic_id: int) -> asyncpg.Record | None:
        query = """
            SELECT topic_id, topic, user_id, created_at
            FROM topics
            WHERE topic_id = $1
        """
        pool = await get_pool()
        async with pool.acquire() as conn:
            return await conn.fetchrow(query, topic_id)
        

    @staticmethod
    async def get_topics_by_user(user_id: int) -> list[asyncpg.Record]:
        query = """
            SELECT topic_id, topic, user_id, created_at
            FROM topics
            WHERE user_id = $1
            ORDER BY created_at DESC
        """
        pool = await get_pool()
        async with pool.acquire() as conn:
            return await conn.fetch(query, user_id)

    @staticmethod
    async def update_topic_title(topic_id: int, topic: str) -> asyncpg.Record | None:
        query = """
            UPDATE topics
            SET topic = $2
            WHERE topic_id = $1
            RETURNING topic_id, topic, user_id, created_at
        """
        pool = await get_pool()
        async with pool.acquire() as conn:
            return await conn.fetchrow(query, topic_id, topic)

    @staticmethod
    async def delete_topic(topic_id: int) -> str:
        query = """
            DELETE FROM topics
            WHERE topic_id = $1
        """
        pool = await get_pool()
        async with pool.acquire() as conn:
            return await conn.execute(query, topic_id)