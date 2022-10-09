from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, models, schemas, utils, oauth2

router = APIRouter(tags=["Authentication"])

@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    #schemas.UserLogin yerine form koyduk burada email yok onun yerine username var
    #Postman'da body degil form-data ya koyacaksin artik

    if not database.table_exists("users"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table does not exist")

    users = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    # Check user exists
    if not users:   
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")

    # Check password is correct
    if not utils.verify_password(user_credentials.password, users.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")

    access_token = oauth2.create_access_token( data= {"user_id" : users.id})

    return {"access_token": access_token, "token_type" : "bearer"}