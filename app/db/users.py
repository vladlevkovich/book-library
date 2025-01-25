from typing import Optional
from .db_connect import db_connect
import asyncpg

async def init_users_db():
    try:
        conn = await asyncpg.connect(user='postgres', password='admin', database='books', host='localhost', port=5432)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    except Exception as e:
        return e

async def add_user(email: str, password: str, test: Optional[bool] = False):
    try:
        conn = await db_connect(test)
        return await conn.execute("""
            INSERT INTO users (email, password) VALUES ($1, $2) ON CONFLICT (email) DO NOTHING RETURNING id
        """, email, password)
    except Exception as e:
        return e

async def get_user(user_email, test: Optional[bool] = False):
    try:
        conn = await db_connect(test)
        return await conn.fetchrow("""
            SELECT * FROM users WHERE email = $1
        """, user_email)
    except Exception as e:
        return e


