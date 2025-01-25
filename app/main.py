from fastapi import FastAPI, HTTPException, status, Request
from contextlib import asynccontextmanager
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.utils.limiter import limiter
from .routers import users, books
from app.db.books import init_books_db
from app.db.users import init_users_db
import asyncio

@asynccontextmanager
async def on_startup(app: FastAPI):
    await init_users_db()
    await init_books_db()
    yield

app = FastAPI(lifespan=on_startup)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(users.router)
app.include_router(books.router)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    raise HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail='Rate limit exceeded. Try again later.'
    )
