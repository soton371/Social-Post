from .database import Base
from sqlalchemy import Column, String, Integer, Boolean

class POst(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=True)
    content = Column(String, nullable=True)
    published = Column(Boolean, default= True)
    