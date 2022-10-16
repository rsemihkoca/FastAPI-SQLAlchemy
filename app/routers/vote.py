from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, database, oauth2


router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(vote: schemas.VoteCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    if not database.table_exists("votes"):
        raise HTTPException(status_code=status.HTTP_NOT_FOUND, detail="Table does not exist")

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist")

    vote_query = db.query(models.Vote).filter(models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id)
    found_vote = vote_query.first()
    if vote.direction == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User {current_user.id} has already voted for post {vote.post_id}")
        else:
            new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
            db.add(new_vote)
            db.commit()
            db.refresh(new_vote)
            return {"message": f"User {current_user.id} has voted for post {vote.post_id}"}
    
    else: #vote.direction == 0:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User {current_user.id} has not voted for post {vote.post_id}")
        else:
            vote_query.delete()
            db.commit()
            return {"message": f"User {current_user.id} has unvoted for post {vote.post_id}"}


