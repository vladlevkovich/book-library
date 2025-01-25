from unittest.mock import AsyncMock, patch
from app.db.books import get_author, insert_author
from .conftest import mock_db_connect
import pytest


@pytest.mark.asyncio
async def test_get_author(mock_db_connect):
    mock_row = {'id': 1, 'name': 'Author1'}
    mock_db_connect.fetchrow.return_value = mock_row

    with patch('app.db.books.db_connect', return_value=mock_db_connect):
        author = await get_author('Author1')

    assert author == mock_row
    mock_db_connect.fetchrow.assert_called_once_with(
        """
            SELECT * FROM authors WHERE name=$1
        """,
        "Author1"
    )

@pytest.mark.asyncio
async def test_insert_author(mock_db_connect):
    mock_db_connect.execute.return_value = 1

    with patch('app.db.books.db_connect', return_value=mock_db_connect):
        result = await insert_author('Author1')

    assert result == {'id': 1, 'name': 'Author1'}
    mock_db_connect.execute.assert_called_once_with(
        """
            INSERT INTO authors (name) VALUES ($1) ON CONFLICT (name) DO NOTHING RETURNING id
        """,
        'Author1'
    )


