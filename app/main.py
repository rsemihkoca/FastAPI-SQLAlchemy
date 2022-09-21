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

#Main route
@app.get("/")
async def root():
    return {"message": "Hello World"}

#Get all posts
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    ### first check if table exists
    if not table_exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, content="Table does not exist")
    
    posts = db.query(models.Post).all()
    return {"data": posts}
