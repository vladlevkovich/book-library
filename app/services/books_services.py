from typing import Optional
from app.db.books import insert_book, get_author, get_filtered_books, update_book_data, insert_author
from app.schemas.books_schemas import BookSchema, BookUpdateSchema
import json

async def get_books(
        author_name: Optional[str] = None,
        genre: Optional[str] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        test: bool = False
):
    try:
        books = await get_filtered_books(author_name, genre, year_from, year_to, test)
        return books
    except Exception as e:
        return {'message': e}

async def new_book(data: BookSchema, test: bool):
    try:
        author = await get_author(data.author_name, test)
        if 'message' in author:
            author = await insert_author(data.author_name, test)
        print(author)
        return await insert_book(data.title, author['id'], data.published_year, data.genre, test)
    except Exception as e:
        return {'error': str(e)}

async def update(data: BookUpdateSchema, book_id: int, test: bool):
    try:
        author = await get_author(data.author_name, test)
        return await update_book_data(book_id, data.title, author['id'], data.published_year, data.genre, test)
    except Exception as e:
        return {'message': e}

async def process_import_books(file, test: Optional[bool] = False):
    try:
        file_content = await file.read()
        if file.content_type not in 'application/json':
            raise Exception('Unsupported file type. Please upload a JSON file.')

        data = json.loads(file_content)
        required_columns = {'title', 'author_name', 'published_year', 'genre'}
        for item in data:
            if not required_columns.issubset(item.keys()):
                raise Exception(f"Missing required columns in item: {item}. Required: {', '.join(required_columns)}")
            author = await get_author(item['author_name'], test)
            await insert_book(item['title'], author['id'], item['published_year'], item['genre'])

        return {'message': 'Books imported successfully'}
    except Exception as e:
        print(f'ERROR: {e}')
        return {'message': str(e)}
