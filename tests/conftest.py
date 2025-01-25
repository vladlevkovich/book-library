import pytest
import httpx
import asyncio
import pytest_asyncio
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from app.db.db_connect import db_connect

@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope='module')
def mock_db_connect():
    mock_conn = AsyncMock()
    mock_conn.fetch.return_value = []
    mock_conn.execute.return_value = 1
    return mock_conn

@pytest_asyncio.fixture(scope="module")
async def client():
    async with httpx.AsyncClient(base_url='http://127.0.0.1:8000') as c:
        yield c

@pytest_asyncio.fixture(scope='module')
async def setup_test_db():
    conn = await db_connect(test=True)
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS authors (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE
            );
            
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author_id INT NOT NULL REFERENCES authors(id) ON DELETE CASCADE,
            published_year INT CHECK(published_year BETWEEN 1800 AND EXTRACT(YEAR FROM CURRENT_DATE)),
            genre VARCHAR(50) CHECK(genre IN ('Fiction', 'Non-fiction', 'Science', 'History', 'Fantasy')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    yield conn

    await conn.execute("DROP TABLE IF EXISTS books, authors, users;")
    await conn.close()
