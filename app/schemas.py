from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: bool = True
    
    
class PostCreate(PostBase):
    pass

# if wanna update specific value then
# class PostUpdate(PostBase):

class Post(PostBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True