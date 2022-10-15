from fastapi import FastAPI

from . import models

from .database import engine, get_db, table_exists
from .routers import post, user, auth
from .configs import settings


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


#Main route
@app.get("/")
async def root():
    return {"message": "Hello World"}



