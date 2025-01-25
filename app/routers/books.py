from fastapi import APIRouter, Depends, HTTPException, status, Request, UploadFile, File
from typing import Optional
from app.services.books_services import get_books
from app.db.books import book_retrieve, book_delete, insert_author
from app.schemas.books_schemas import BookSchema, BookUpdateSchema, AuthorSchema
from app.utils.auth import get_current_user
from app.services.books_services import new_book, update, process_import_books
from .responses import books_response, add_book_response, book_detail_response, book_update_responses, book_delete_responses, books_import_responses
from app.utils.limiter import limiter

router = APIRouter(prefix='/books')

@router.get('/books', responses=books_response)
@limiter.limit('100/minute')
async def books(
        request: Request,
        author_name: Optional[str] = None,
        genre: Optional[str] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        test: bool = False
):
    return await get_books(author_name, genre, year_from, year_to, test)

@router.post('/add-book', responses=add_book_response)
@limiter.limit('100/minute')
async def add_book(request: Request, data: BookSchema, test: bool = False, current_user = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')
    return await new_book(data, test)

@router.post('/add-author')
@limiter.limit('100/minute')
async def add_author(request: Request, data: AuthorSchema, current_user: dict = Depends(get_current_user), test: Optional[bool] = False):
    try:
        if not current_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')
        await insert_author(data.name, test)
        return {'message': 'Author added'}
    except Exception as e:
        return {'message': str(e)}

@router.get('/book/{book_id}', responses=book_detail_response)
@limiter.limit('100/minute')
async def get_book(request: Request, book_id: int, test: bool = False):
    return await book_retrieve(book_id, test)

@router.put('/update/{book_id}', responses=book_update_responses)
@limiter.limit('100/minute')
async def book_update(request: Request, data: BookUpdateSchema, book_id: int, test: Optional[bool] = False, current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')
    return await update(data, book_id, test)

@router.delete('/delete/{book_id}', responses=book_delete_responses)
@limiter.limit('100/minute')
async def delete_book(request: Request, book_id: int, test: bool = False, current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized'
        )
    result = await book_delete(book_id, test)
    if result == 'DELETE 0':
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )
    return {'message': 'Deleted'}

@router.post('/books-json-import', responses=books_import_responses)
async def books_import(test: Optional[bool] = False, current_user: dict = Depends(get_current_user), file: UploadFile = File(...)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')
    return await process_import_books(file, test)
