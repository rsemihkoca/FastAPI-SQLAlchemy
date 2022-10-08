from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
from sqlalchemy.orm import Session

import sys, os, pprint
from . import models, schemas, utils

from .database import engine, get_db, table_exists
from .routers import post, user, auth



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


#Main route
@app.get("/")
async def root():
    return {"message": "Hello World"}



