from fastapi import status, HTTPException, Depends, APIRouter, Response
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(tags=['Authentication'])


@router.post("/login", response_model=schemas.Token)
# def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # verify = utils.verify(user_credentials.password, user.password)
    verify = utils.verify(user_credentials.password, user.password)
    if not verify:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")

    # create token & return token
    accessToken = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": accessToken, "token_type": "Bearer"}
