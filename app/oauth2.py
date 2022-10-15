from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, models, database
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .configs import settings

oauth2_scheme  = OAuth2PasswordBearer(tokenUrl="login")

# to get a string like this run:
# ı
SECRET_KEY = settings.secret_key
ALGORITHM =  settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes



def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire

    encoded_JWT = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)

    return encoded_JWT

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        user_id = payload.get("user_id") # user_id: int = payload.get("user_id") seklindeydi
        if user_id is None:
            raise JWTError
        token_data = schemas.TokenData(user_id = user_id)
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token_data = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token_data.user_id).first()

    if user is None:
        raise credentials_exception
    
    return user


