from pydantic import BaseModel, EmailStr
from typing import Optional


class UserOut(BaseModel):
    id: int
    email: EmailStr

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostReturn(Post):
    id: int
    owner_id: int
    owner: UserOut

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type:str

class TokenData(BaseModel):
    id: Optional[int] = None