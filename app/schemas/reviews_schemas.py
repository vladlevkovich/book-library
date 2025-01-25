from pydantic import BaseModel
from typing import Optional

class ReviewSchema(BaseModel):
    book_id: int
    user_id: int
    comment: Optional[str] = None
