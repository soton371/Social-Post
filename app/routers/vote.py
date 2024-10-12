from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2, database
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/vote',
    tags=['Vote']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def vote(vote: schemas.Vote, db: Session = Depends(database.get_db),
               current_user: int = Depends(oauth2.get_current_user)):

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if vote.dir == 1:  # 1 vote add 0 vote delete
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {
                                current_user.id} has already voted on post {vote.post_id}"
                                )
        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted vote"}
