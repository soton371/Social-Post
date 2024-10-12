from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic.types import conint

class PostBase(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: bool = True
    
    
class PostCreate(PostBase):
    pass

# if wanna update specific value then
# class PostUpdate(PostBase):

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    
    class Config:
        from_attributes = True
        
        
# for user
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    

        
        
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None



class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)