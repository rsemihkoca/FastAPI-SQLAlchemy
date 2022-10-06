from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db, table_exists
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post)
app.include_router(user)

#Main route
@app.get("/")
async def root():
    return {"message": "Hello World"}



