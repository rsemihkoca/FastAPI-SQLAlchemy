from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, models
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme  = OAuth2PasswordBearer(tokenUrl="login")

# to get a string like this run:
# ı
SECRET_KEY = "aa5a6676780645d6642eb686e535452ac5934793f60b3c1f80fd56328597f054"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire

    encoded_JWT = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)

    return encoded_JWT

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise JWTError
        token_data = schemas.TokenData(user_id = user_id)
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, credentials_exception)

