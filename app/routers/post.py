from fastapi import status, HTTPException, Depends, APIRouter
from typing import List
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), 
                      current_user: int = Depends(oauth2.get_current_user)):
    try:
        # new_post = models.Post(title = post.title, content = post.content, published = post.published)
        new_post = models.Post(owner_id = current_user, **post.model_dump())  # ** unpacked
        db.add(new_post)
        db.commit()
        db.refresh(new_post)

        return new_post
    except Exception as error:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))


@router.get("/{id}", response_model=schemas.Post)
async def single_post(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post not found with {id}')
    return post


@router.delete("/{id}")
async def delete_post(id: int, db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post not found with {id}')
    
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to preform request action')
    
    post.delete(synchronize_session=False)
    db.commit()
    return {"message": "Post deleted successfully"}


@router.put("/{id}")
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), 
                      current_user: int = Depends(oauth2.get_current_user)):
    postQuery = db.query(models.Post).filter(models.Post.id == id)
    updatedPost = postQuery.first()
    if not updatedPost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post not found with {id}')
    postQuery.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return {"message": "Post updated successfully"}
