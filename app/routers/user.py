from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users"
)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        hashedPassword = utils.hash(user.password)
        user.password = hashedPassword
        new_user = models.User(**user.model_dump())
        db.add(new_user)
        db.commit() 
        db.refresh(new_user)
        
        return new_user
    except Exception as error:
        return HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)) 
    

@router.get("/{id}", response_model= schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist")
    
    return user

