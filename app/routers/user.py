
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, utils
from ..database import get_db, table_exists





router = APIRouter()

#Create a new user
@router.post("/users",status_code = status.HTTP_201_CREATED, response_model= schemas.UserOut)
async def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):

    if not table_exists("users"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, content="Table does not exist")  # type: ignore

    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    NewUser = models.User(**user.dict())
    db.add(NewUser)
    db.commit() 
    db.refresh(NewUser)  ## Posgre Duplice mail internal error nasıl exception yapılır

    return NewUser  

#Get a single user(FIND)
@router.get("/users/{id}", status_code = status.HTTP_302_FOUND, response_model = schemas.UserOut)
async def get_user(id: int, db: Session = Depends(get_db)):

    if not table_exists("users"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, content="Table does not exist")  # type: ignore

    users = db.query(models.User).filter(models.User.id == id).first() # all değil first çünkü tek bir kayıt döndürüyoruz

    if not users:   
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")

    return users

#Get all posts
@router.get("/users", response_model=List[schemas.UserOut])
async def get_users(db: Session = Depends(get_db)):
    ### first check if table exists
    if not table_exists("users"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, content="Table does not exist")  # type: ignore
    
    users = db.query(models.User).all()
    return users