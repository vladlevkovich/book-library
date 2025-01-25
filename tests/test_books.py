from unittest.mock import AsyncMock, patch
from app.db.books import insert_book, book_retrieve, get_filtered_books
from .conftest import mock_db_connect, client, setup_test_db
from app.utils.auth import create_access_token
import pytest

@pytest.mark.asyncio
async def test_get_books(client, setup_test_db):
    response = await client.get('/books/books?genre=Fiction&test=True')
    data = response.json()
    assert response.status_code == 200
    for item in data:
        assert item['genre'] == 'Fiction'

@pytest.mark.asyncio
async def test_author_insert(client, setup_test_db):
    author_data = {'name': 'Author1'}
    expected_result = {'message': 'Author added'}
    mock_current_user = {'id': 1, 'email': 'email@gmail.com'}
    auth_token = create_access_token(mock_current_user)
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = await client.post('/books/add-author?test=True', json=author_data, headers=headers)
    assert response.json() == expected_result


@pytest.mark.asyncio
async def test_add_book(client, setup_test_db):
    mock_current_user = {'id': 1, 'email': 'email@gmail.com'}
    book_data = {
        'title': 'Harry Potter',
        'author_name': 'Author1',
        'published_year': 2000,
        'genre': 'Science'
    }

    expected_result = {'message': 'Book added'}
    auth_token = create_access_token(mock_current_user)
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = await client.post('/books/add-book?test=True', json=book_data, headers=headers)
    print('JSON', response.json())
    assert response.status_code == 200
    assert response.json() == expected_result


@pytest.mark.asyncio
async def test_delete_book(client, setup_test_db):
    expected_result = {'message': 'Deleted'}
    mock_current_user = {'id': 4, 'email': 'email@gmail.com'}
    auth_token = create_access_token(mock_current_user)
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = await client.delete('/books/delete/13?test=True', headers=headers)

    assert response.status_code == 200
    assert response.json() == expected_result

@pytest.mark.asyncio
async def test_update_book(client, mock_db_connect):
    mock_current_user = {'id': 4, 'email': 'email@gmail.com'}
    book_data = {
        'title': 'Book Update',
        'author_name': 'Author1',
        'published_year': 2023,
        'genre': 'Science',
    }
    expected_result = {'message': 'Data updated'}
    auth_token = create_access_token(mock_current_user)
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = await client.put('/books/update/13?test=True', json=book_data, headers=headers)
    data = response.json()

    assert response.status_code == 200
    assert data == expected_result

@pytest.mark.asyncio
async def test_insert_book(mock_db_connect):
    mock_db_connect.mock_conn.execute.return_value = 1
    title = 'Book1'
    author_id = 1
    published_year = 1800
    genre = 'Fiction'

    with patch('app.db.books.db_connect', return_value=mock_db_connect):
        result = await insert_book(title, author_id, published_year, genre)

    assert result == {'message': 'Book added'}
    mock_db_connect.execute.assert_called_once_with(
        """
            INSERT INTO books (title, author_id, published_year, genre)
            VALUES ($1, $2, $3, $4)
        """, title, author_id, published_year, genre
    )

@pytest.mark.asyncio
async def test_insert_book_invalid_year(mock_db_connect):
    mock_db_connect.mock_conn.execute.return_value = 1
    title = 'Book1'
    author_id = 1
    published_year = 1799
    genre = 'Fiction'

    with patch('app.db.books.db_connect', return_value=mock_db_connect):
        result = await insert_book(title, author_id, published_year, genre)

    assert isinstance(result, ValueError)
    assert str(result) == "Published year must be between 1800 and 2025"

