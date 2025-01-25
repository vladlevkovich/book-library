import pytest
from unittest.mock import patch
from .conftest import client, setup_test_db


@pytest.mark.asyncio
async def test_user_register(client, setup_test_db):
    user_data = {'email': 'test@gmail.com', 'password': '123'}
    expected_result = {'message': 'User register'}
    response = await client.post('users/register?test=True', json=user_data)
    data = response.json()

    assert response.status_code == 200
    assert data == expected_result

@pytest.mark.asyncio
async def test_user_login(client, setup_test_db):
    user_data = {'email': 'test@gmail.com', 'password': '123'}
    response = await client.post('/users/login?test=True', json=user_data)
    data = response.json()
    print('data', data)
    assert response.status_code == 200
    assert data['type'] == 'bearer'

