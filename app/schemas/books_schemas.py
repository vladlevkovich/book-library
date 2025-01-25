from pydantic import BaseModel

class BookSchema(BaseModel):
    title: str
    author_name: str
    published_year: int
    genre: str


class BookUpdateSchema(BookSchema):
    pass


class AuthorSchema(BaseModel):
    name: str
