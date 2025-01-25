from fastapi import Depends, HTTPException, status
from datetime import timedelta, datetime, timezone
from jwt.exceptions import PyJWTError
from app.schemas.auth_schema import DataToken
from app.db.users import get_user
from .common import oauth2_schema
import jwt

SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE = 30

def create_access_token(data: dict, expire_delta: timedelta | None = None):
    payload = data.copy()
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    payload.update({'exp': expire})
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token_access(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get('id')
        email = payload.get('email')
        if user_id is None:
            raise credential_exception
        token_data = DataToken(id=user_id, email=email)
        return token_data
    except PyJWTError as e:
        print(e)
        raise credential_exception

async def get_current_user(token: str = Depends(oauth2_schema)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    token = verify_token_access(token, credential_exception)
    user = await get_user(token.email)
    return {
        'id': user['id'],
        'email': user['email']
    }

