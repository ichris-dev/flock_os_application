import asyncpg
from app.db.db_connection import get_pool


class MessagesRepository:
    """Owns all SQL for the messages table. The API layer talks to this,
    never to asyncpg directly."""

    @staticmethod
    async def create_message(
        topic_id: int,
        is_user: bool,
        content: str,
    ) -> asyncpg.Record:
        query = """
            INSERT INTO messages (topic_id, is_user, content)
            VALUES ($1, $2, $3)
            RETURNING message_id, topic_id, is_user, content, created_at
        """
        pool = await get_pool()
        async with pool.acquire() as conn:
            return await conn.fetchrow(query, topic_id, is_user, content)

    @staticmethod
    async def get_messages_by_topic(topic_id: int) -> list[asyncpg.Record]:
        query = """
            SELECT message_id, topic_id, is_user, content, created_at
            FROM messages
            WHERE topic_id = $1
            ORDER BY created_at ASC
        """
        pool = await get_pool()
        async with pool.acquire() as conn:
            return await conn.fetch(query, topic_id)

    @staticmethod
    async def get_message_by_id(message_id: int) -> asyncpg.Record | None:
        query = """
            SELECT message_id, topic_id, is_user, content, created_at
            FROM messages
            WHERE message_id = $1
        """
        pool = await get_pool()
        async with pool.acquire() as conn:
            return await conn.fetchrow(query, message_id)

    @staticmethod
    async def delete_messages_by_topic(topic_id: int) -> str:
        query = """
            DELETE FROM messages
            WHERE topic_id = $1
        """
        pool = await get_pool()
        async with pool.acquire() as conn:
            return await conn.execute(query, topic_id)