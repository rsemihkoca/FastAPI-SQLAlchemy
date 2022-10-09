
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from fastapi.params import Body
from .. import models, schemas, oauth2
from ..database import get_db, table_exists



router = APIRouter(
    prefix="/posts",   # Final'da kaldır çünkü kod okumayı zorlaştırıyor
    tags=["Posts"]
    )

#Get all posts
@router.get("/", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    ### first check if table exists
    if not table_exists("posts"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table does not exist")  # type: ignore
    
    posts = db.query(models.Post).all()
    return posts

#Create a new post
@router.post("/",status_code = status.HTTP_201_CREATED, response_model = schemas.Post)
async def create_posts(post: schemas.PostCreate = Body(...), db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):  # type: ignore
    if not table_exists("posts"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table does not exist")  # type: ignore
    
    #NewPost = models.Post(title=post.title, detail=post.detail, published=post.published)
    NewPost = models.Post(**post.dict())
    #connection.commit() : commit işlemi burada böyle:
    db.add(NewPost)
    db.commit() 
    db.refresh(NewPost)  # RETURNING * gibi

    return NewPost

#Get a single post(FIND)
@router.get("/{id}", status_code = status.HTTP_302_FOUND, response_model = schemas.Post)
async def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    if not table_exists("posts"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table does not exist")  # type: ignore

    posts = db.query(models.Post).filter(models.Post.id == id).first() # all değil first çünkü tek bir kayıt döndürüyoruz

    if not posts:   
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    return posts

#Delete Post
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    if not table_exists("posts"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table does not exist")  # type: ignore

    posts = db.query(models.Post).filter(models.Post.id == id) # all değil first çünkü tek bir kayıt döndürüyoruz

    if not posts.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    posts.delete(synchronize_session=False)
    db.commit()
    
    return f"Post with id {id} is deleted"

#Update Post
@router.put("/{id}", status_code = status.HTTP_202_ACCEPTED, response_model = schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    if not table_exists("posts"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table does not exist")  # type: ignore


    post_query = db.query(models.Post).filter(models.Post.id == id) # all değil first çünkü tek bir kayıt döndürüyoruz

    posts = post_query.first()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    post_query.update(post.dict(),synchronize_session=False)
    db.commit()

    return post_query.first()