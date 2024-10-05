from fastapi import FastAPI, status, HTTPException, Depends

from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"message": "Post fetched successfully", "data" : posts}


@app.post("/posts", status_code = status.HTTP_201_CREATED, response_model= schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    try:
        # new_post = models.Post(title = post.title, content = post.content, published = post.published)
        new_post = models.Post(**post.model_dump()) #** unpacked
        db.add(new_post)
        db.commit() 
        db.refresh(new_post)
        
        return new_post
    except Exception as error:
        return HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)) 



@app.get("/posts/{id}")
async def single_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f'Post not found with {id}') 
    return {"message": "Post fetched successfully", "data" : post}



@app.delete("/posts/{id}")
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f'Post not found with {id}') 
    post.delete(synchronize_session= False)
    db.commit()
    return {"message": "Post deleted successfully"}


@app.put("/posts/{id}")
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    postQuery = db.query(models.Post).filter(models.Post.id == id)
    updatedPost = postQuery.first()
    if not updatedPost:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f'Post not found with {id}') 
    postQuery.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return {"message": "Post updated successfully", "data" : postQuery.first()}

# 4:30