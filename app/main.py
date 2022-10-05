from tkinter import N
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db, table_exists

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Main route
@app.get("/")
async def root():
    return {"message": "Hello World"}

#Get all posts
@app.get("/posts", response_model=list[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    ### first check if table exists
    if not table_exists("posts"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, content="Table does not exist")  # type: ignore
    
    posts = db.query(models.Post).all()
    return posts

#Create a new post
@app.post("/posts",status_code = status.HTTP_201_CREATED, response_model = schemas.Post)
async def create_posts(post: schemas.PostCreate = Body(...), db: Session = Depends(get_db)):  # type: ignore
    if not table_exists("posts"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, content="Table does not exist")  # type: ignore
    
    #NewPost = models.Post(title=post.title, content=post.content, published=post.published)
    NewPost = models.Post(**post.dict())
    #connection.commit() : commit işlemi burada böyle:
    db.add(NewPost)
    db.commit() 
    db.refresh(NewPost)  # RETURNING * gibi

    return NewPost

#Get a single post(FIND)
@app.get("/posts/{id}", status_code = status.HTTP_302_FOUND, response_model = schemas.Post)
async def get_post(id: int, db: Session = Depends(get_db)):

    if not table_exists("posts"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, content="Table does not exist")  # type: ignore

    posts = db.query(models.Post).filter(models.Post.id == id).first() # all değil first çünkü tek bir kayıt döndürüyoruz

    if not posts:   
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    return posts

#Delete Post
@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    if not table_exists("posts"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, content="Table does not exist")  # type: ignore

    posts = db.query(models.Post).filter(models.Post.id == id) # all değil first çünkü tek bir kayıt döndürüyoruz

    if not posts.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    posts.delete(synchronize_session=False)
    db.commit()

    return posts

#Update Post
@app.put("/posts/{id}", status_code = status.HTTP_202_ACCEPTED, response_model = schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):

    if not table_exists("posts"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, content="Table does not exist")  # type: ignore


    post_query = db.query(models.Post).filter(models.Post.id == id) # all değil first çünkü tek bir kayıt döndürüyoruz

    posts = post_query.first()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    post_query.update(post.dict(),synchronize_session=False)
    db.commit()

    return post_query.first()


#Create a new user
@app.post("/users",status_code = status.HTTP_201_CREATED, response_model= schemas.UserOut)
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
