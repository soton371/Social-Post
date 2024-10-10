import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    toEncode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    toEncode.update({"exp": expire})

    return jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str, credential_exception):
    try:
        print(f"token: {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = str(payload.get('user_id'))

        print(f"id: {id}")

        if id is None:
            raise credential_exception

        token_data = schemas.TokenData(id=id)
    except Exception as e:
        print(f"error: {e}")
        raise credential_exception
    
    return token_data



def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credential", headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, credential_exception)