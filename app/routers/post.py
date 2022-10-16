
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from fastapi.params import Body
from .. import models, schemas, oauth2, database



router = APIRouter(
    prefix="/posts",   # Final'da kaldır çünkü kod okumayı zorlaştırıyor
    tags=["Posts"]
    )

#Get all posts
@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(
                    db: Session = Depends(database.get_db), 
                    current_user: int = Depends(oauth2.get_current_user), 
                    skip: Optional[int] = 0 , 
                    limit: Optional[int] = 100,
                    search: Optional[str] = ""
                    ):

    if not database.table_exists("posts"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table does not exist")  # type: ignore
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id).group_by(models.Post.id).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()

    return posts


#Get All Posts of a User
@router.get("/user/{user_id}", response_model=List[schemas.PostOut])
async def get_posts_by_user(user_id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    ### first check if table exists
    if not database.table_exists("posts"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table does not exist")

    # eğer bir kullanıcı başkasının postlarını görmemeli ise user_id ile gelen id current_user ile aynı olmalı 
    # if not user_id == current_user: 
    #   raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only see your own posts") # type: ignore
        #posts = db.query(models.Post).filter(models.Post.owner_id == user_id).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id).group_by(models.Post.id).filter(models.Post.owner_id == user_id).all()


    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} does not have any posts yet")

    return posts

#Create a new post
@router.post("/",status_code = status.HTTP_201_CREATED, response_model = schemas.Post)
async def create_posts(post: schemas.PostCreate = Body(...), db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):  # type: ignore
    if not database.table_exists("posts"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table does not exist")  # type: ignore
    
    #NewPost = models.Post(title=post.title, detail=post.detail, published=post.published)
    NewPost = models.Post(owner_id = current_user.id, **post.dict())   # type: ignore
    #connection.commit() : commit işlemi burada böyle:
    db.add(NewPost)
    db.commit() 
    db.refresh(NewPost)  # RETURNING * gibi

    return NewPost

#Get a single post(FIND)
@router.get("/{id}", status_code = status.HTTP_302_FOUND, response_model = schemas.PostOut)
async def get_post(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    if not database.table_exists("posts"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table does not exist")  # type: ignore

    # all değil first çünkü tek bir kayıt döndürüyoruz
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not posts:   
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    return posts

#Delete Post
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    if not database.table_exists("posts"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table does not exist")  # type: ignore

    posts_query = db.query(models.Post).filter(models.Post.id == id) # all değil first çünkü tek bir kayıt döndürüyoruz

    post = posts_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    # Eğer post sahibi değilse silme işlemi yapma
    if post.owner_id != current_user.id:  # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not the owner of this post")

    posts_query.delete(synchronize_session=False)
    db.commit()
    
    return f"Post with id {id} is deleted"

#Update Post
@router.put("/{id}", status_code = status.HTTP_202_ACCEPTED, response_model = schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    if not database.table_exists("posts"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table does not exist")  # type: ignore


    post_query = db.query(models.Post).filter(models.Post.id == id) # all değil first çünkü tek bir kayıt döndürüyoruz

    posts = post_query.first()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    if posts.owner_id != current_user.id:  # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not the owner of this post")

    post_query.update(post.dict(),synchronize_session=False)
    db.commit()

    return posts