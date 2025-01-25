from fastapi import FastAPI, HTTPException, status, Request
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.utils.limiter import limiter
from .routers import users, books
from app.db.books import init_books_db
from app.db.users import init_users_db
import asyncio

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# asyncio.run(init_users_db())
# asyncio.run(init_books_db())

app.include_router(users.router)
app.include_router(books.router)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    raise HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail='Rate limit exceeded. Try again later.'
    )

