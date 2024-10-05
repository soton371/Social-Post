from .database import Base
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean, server_default= "TRUE")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))