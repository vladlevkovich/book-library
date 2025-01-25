from typing import Optional
from .db_connect import db_connect
import asyncpg

async def init_books_db():
    try:
        conn = await asyncpg.connect(user='postgres', password='admin', database='books', host='localhost', port=5432)
        await conn.execute('''
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
        ''')
        await conn.close()
    except Exception as e:
        return e

async def get_author(name: str, test: Optional[bool] = False):
    try:
        conn = await db_connect(test)
        author = await conn.fetchrow("""
            SELECT * FROM authors WHERE name=$1
        """, name)
        print('AUTHOR', author)
        if not author:
            print('IF')
            return {'message': 'Author not found'}
        return dict(author)
    except Exception as e:
        return {'error': str(e)}

async def insert_author(name, test: Optional[bool] = False):
    try:
        conn = await db_connect(test)
        await conn.execute("""
            INSERT INTO authors (name) VALUES ($1) ON CONFLICT (name) DO NOTHING RETURNING id
        """, name)
        return await get_author(name, test)
    except Exception as e:
        return e

async def get_filtered_books(author_name=None, genre=None, year_from=None, year_to=None, test: bool = False):
    try:
        conn = await db_connect(test)
        query = """
            SELECT books.id, books.title, books.published_year, books.genre, 
            books.created_at, books.updated_at, authors.name AS author_name
            FROM books
            JOIN authors ON books.author_id = authors.id
            WHERE 1=1
        """
        params = []
        param_index = 1
        if author_name:
            query += f" AND authors.name ILIKE ${param_index}"
            params.append(f"%{author_name}%")
            param_index += 1
        if genre:
            query += f" AND books.genre = ${param_index}"
            params.append(genre)
            param_index += 1
        if year_from:
            query += f" AND books.published_year >= ${param_index}"
            params.append(year_from)
            param_index += 1
        if year_to:
            query += f" AND books.published_year <= ${param_index}"
            params.append(year_to)
            param_index += 1
        query += " ORDER BY books.published_year DESC"
        books = await conn.fetch(query, *params)
        return [dict(book) for book in books]
    except Exception as e:
        print(f'ERROR: {e}')
        return e

async def book_retrieve(book_id: int, test: bool):
    try:
        conn = await db_connect(test)
        # return await conn.fetchrow("""
        #     SELECT * FROM books WHERE id=$1
        # """, book_id)
        query = """
                    SELECT books.id, books.title, books.published_year, books.genre, 
                    books.created_at, books.updated_at, authors.name AS author_name
                    FROM books
                    JOIN authors ON books.author_id = authors.id
                    WHERE books.id = $1
                """
        # Виконання запиту
        book = await conn.fetchrow(query, book_id)
        if not book:
            return {'message': 'Book not found'}
            # Повертаємо результат як словник
        return dict(book)
    except Exception as e:
        print(f'ERROR: {e}')
        return e

async def insert_book(title: str, author_id: int, published_year: int, genre: str, test: Optional[bool] = False):
    try:
        current_year = 2025
        if not (1800 <= published_year <= current_year):
            raise ValueError(f"Published year must be between 1800 and {current_year}")
        conn = await db_connect(test)
        await conn.execute("""
            INSERT INTO books (title, author_id, published_year, genre)
            VALUES ($1, $2, $3, $4)
        """, title, author_id, published_year, genre)
        return {'message': 'Book added'}
    except Exception as e:
        return e

async def update_book_data(
        book_id: int,
        title:str = None,
        author_id: int = None,
        published_year: int = None,
        genre: str = None,
        test: bool = False
):
    conn = await db_connect(test)
    try:
        await conn.execute("""
            UPDATE books SET title=$1, author_id=$2, published_year=$3, genre=$4 WHERE id=$5
        """, title, author_id, published_year, genre, book_id)
        return {'message': 'Data updated'}
    except Exception as e:
        print(f'ERROR: {e}')
        return e
    finally:
        conn.close()

async def book_delete(book_id: int, test: bool):
    conn = await db_connect(test)
    try:
        await conn.execute("""
            DELETE FROM books WHERE id=$1
        """, book_id)
        return {'message': 'Deleted'}
    except Exception as e:
        print(f'ERROR: {e}')
        return e
