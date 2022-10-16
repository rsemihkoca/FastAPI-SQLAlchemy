from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime

from app.database import Base


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    created_at: datetime
    email: EmailStr

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    user_id: int

class VoteCreate(BaseModel):
    post_id: int
    direction: conint(le=1) # conint(ge=-1, le=1) yaparak dislike yapma bilgisini de dene

""" class VoteOut(BaseModel):
    id: int
    created_at: datetime
    user_id: int
    post_id: int

    class Config:
        orm_mode = True """