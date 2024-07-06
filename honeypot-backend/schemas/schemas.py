from pydantic import BaseModel, validator
from uuid import UUID, uuid4
from typing import Any

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class User(BaseModel):
    id: UUID
    username: str
    email: str
    password: str

    class Config:
        from_attributes = True

class PostCreate(BaseModel):
    content: str
    comments_number: int
    likes_number: int
    author_id: UUID

    @validator('author_id', pre=True)
    def convert_author_id(cls, value: Any) -> UUID:
        if isinstance(value, str):
            return UUID(value)
        return value

class Post(BaseModel):
    id: UUID
    content: str
    comments_number: int
    likes_number: int
    author_id: UUID

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str
