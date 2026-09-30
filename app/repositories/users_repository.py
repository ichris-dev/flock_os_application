import asyncpg
from app.db.db_connection import get_pool


class UsersRepository:
    """Owns all SQL for the users table. The API layer talks to this,
    never to asyncpg directly."""

    @staticmethod
    async def create_user(
        username: str,
        email_or_phone: str,
        hashed_password: str,
    ) -> asyncpg.Record:
        query = """
            INSERT INTO users (username, email_or_phone, password)
            VALUES ($1, $2, $3)
            RETURNING user_id, username, email_or_phone, created_at
        """

        pool = await get_pool()

        async with pool.acquire() as conn:
            return await conn.fetchrow(
                query,
                username,
                email_or_phone,
                hashed_password,
            )

    @staticmethod
    async def get_user_by_identifier(
        email_or_phone: str,
        password: str,
    ) -> asyncpg.Record | None:
        query = """
            SELECT user_id, username, email_or_phone, password, created_at
            FROM users
            WHERE email_or_phone = $1 AND password = $2
        """

        pool = await get_pool()

        async with pool.acquire() as conn:
            return await conn.fetchrow(
                query,
                email_or_phone,
                password,
            )

    # ----------------------------------------
    # GOOGLE AUTH
    # ----------------------------------------

    @staticmethod
    async def get_user_by_google_id(
        google_id: str,
    ) -> asyncpg.Record | None:
        query = """
            SELECT user_id, username, email_or_phone, created_at
            FROM users
            WHERE google_id = $1
        """

        pool = await get_pool()

        async with pool.acquire() as conn:
            return await conn.fetchrow(query, google_id)

    @staticmethod
    async def get_user_by_email(
        email: str,
    ) -> asyncpg.Record | None:
        query = """
            SELECT user_id, username, email_or_phone, created_at
            FROM users
            WHERE email_or_phone = $1
        """

        pool = await get_pool()

        async with pool.acquire() as conn:
            return await conn.fetchrow(query, email)

    @staticmethod
    async def link_google_account(
        user_id: int,
        google_id: str,
    ) -> asyncpg.Record:
        query = """
            UPDATE users
            SET google_id = $1
            WHERE user_id = $2
            RETURNING user_id, username, email_or_phone, created_at
        """

        pool = await get_pool()

        async with pool.acquire() as conn:
            return await conn.fetchrow(
                query,
                google_id,
                user_id,
            )

    @staticmethod
    async def create_google_user(
        username: str,
        email: str,
        google_id: str,
    ) -> asyncpg.Record:
        query = """
            INSERT INTO users (
                username,
                email_or_phone,
                password,
                google_id
            )
            VALUES ($1, $2, NULL, $3)
            RETURNING user_id, username, email_or_phone, created_at
        """

        pool = await get_pool()

        async with pool.acquire() as conn:
            return await conn.fetchrow(
                query,
                username,
                email,
                google_id,
            )
    
    @staticmethod
    async def get_user_by_username(
        username: str,
    ) -> asyncpg.Record | None:
        query = """
            SELECT user_id, username
            FROM users
            WHERE username = $1
        """

        pool = await get_pool()

        async with pool.acquire() as conn:
            return await conn.fetchrow(query, username)