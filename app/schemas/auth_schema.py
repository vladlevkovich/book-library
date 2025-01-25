from pydantic import BaseModel
from typing import Optional

class DataToken(BaseModel):
    # id: Optional[] = None
    id: Optional[int] = None
    email: Optional[str] = None
