from tkinter import N
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db, table_exists

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

#Main route
@app.get("/")
async def root():
    return {"message": "Hello World"}

#Get all posts
@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    ### first check if table exists
    if not table_exists("posts"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, content="Table does not exist")
    
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.post("/posts",status_code = status.HTTP_201_CREATED,) 
async def create_posts(post: Post = Body(...), db: Session = Depends(get_db)):
    if not table_exists("posts"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, content="Table does not exist")
    
    #NewPost = models.Post(title=post.title, content=post.content, published=post.published)
    NewPost = models.Post(**post.dict())
    #connection.commit() : commit işlemi burada böyle:
    db.add(NewPost)
    db.commit() 
    db.refresh(NewPost)  # RETURNING * gibi

    return {"data": NewPost}
