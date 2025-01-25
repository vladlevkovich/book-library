from fastapi import APIRouter, Request
from typing import Optional
from app.schemas.users_schemas import UserRegisterSchema, UserLoginSchema
from app.services.users_services import register, login
from app.utils.limiter import limiter
from .responses import register_response, login_response

router = APIRouter(prefix='/users')

@router.post('/register', responses=register_response)
@limiter.limit('100/minute')
async def user_register(request: Request, data: UserRegisterSchema, test: Optional[bool] = False):
    return await register(data, test)

@router.post('/login', responses=login_response)
@limiter.limit('100/minute')
async def user_login(request: Request, data: UserLoginSchema, test: Optional[bool] = False):
    return await login(data, test)

# @router.post('/register')
# async def user_register(email: Annotated[str, Form()]):
#     return {'email': email}

