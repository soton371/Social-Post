from fastapi import FastAPI, status, HTTPException, Depends
# connect db
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# model
from pydantic import BaseModel
from typing import Optional

from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# connect db
while True:
    try:
        conn = psycopg2.connect(
            host = 'localhost', 
            database = 'socialpost', 
            user = 'postgres', 
            password = '1234', 
            cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print('DB Connected')
        break
    except Exception as error:
        print(f'DB connection error: {error}')
        time.sleep(2)


class Post(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: bool = True
    


@app.get("/")
async def root():
    return {"message": "Hello World"}

# for test
@app.get("/test-post")
def test_post(db: Session = Depends(get_db)):
    return {"status":"success"}



@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(f'posts: {posts}')
    if posts == []:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail='Empty posts') 
    return {"message": "Post created successfully", "data" : posts}


@app.post("/posts", status_code = status.HTTP_201_CREATED)
async def create_post(post: Post):
    try:
        
        # Works but not safe from hackers
        # cursor.execute(f"INSERT INTO posts (title, content, published) VALUES ({post.title}, {post.content}, 
        #                {post.published})")
        
        # Working and safe from hackers
        cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
                    vars= (post.title, post.content, post.published))
        
        conn.commit()
        
        new_post = cursor.fetchone()
        
        return {"message": "Post created successfully", "data" : new_post}
    except Exception as error:
        return HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)) 



@app.get("/posts/{id}")
async def single_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    print(f"post: {post}")
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail='Post not found') 
    return {"message": "Post fetched successfully", "data" : post}



@app.delete("/posts/{id}")
async def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    post = cursor.fetchone()
    print(f"post: {post}")
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f'Post not found with {id}') 
    conn.commit()
    return {"message": "Post fetched successfully"}


@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
                (post.title, post.content, post.published, str(id)))
    updatedPost = cursor.fetchone()
    if not updatedPost:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f'Post not found with {id}') 
    conn.commit()
    return {"message": "Post updated successfully", "data" : updatedPost}

# 4:30