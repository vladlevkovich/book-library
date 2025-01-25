from fastapi import HTTPException, status
from typing import Optional
from app.utils.common import get_password_hash, verify_password
from app.db.users import add_user, get_user
from app.schemas.users_schemas import UserRegisterSchema, UserLoginSchema
from app.utils.auth import create_access_token

async def register(data: UserRegisterSchema, test: Optional[bool] = False):
    try:
        try:
            password_hash = get_password_hash(data.password)
            user_id = await add_user(data.email, password_hash, test)
            if not user_id:
                raise HTTPException(
                    detail='User with this email already exists',
                    status_code=status.HTTP_409_CONFLICT
                )
            return {'message': 'User register'}
        except Exception as e:
            print(e)
            return e
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)

async def login(data: UserLoginSchema, test: Optional[bool] = False):
    try:
        user = await get_user(data.email, test)
        if not user:
            raise HTTPException(
                detail='User not found!',
                status_code=status.HTTP_404_NOT_FOUND
            )
        if not verify_password(data.password, user['password']):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid data'
            )

        payload = {
            'id': user['id'],
            'email': user['email']
        }
        return {'access_token': create_access_token(payload), 'type': 'bearer'}
    except Exception as e:
        return {'message': e}
