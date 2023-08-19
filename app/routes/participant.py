from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import GetOption, GetParticipant
from app.models import User, Quiz, Question, Option, Participant
from app.utils import hash, check_if_found
from app.oauth2 import get_current_user
from typing import List

router = APIRouter(
    prefix="/participant",
    tags=["Participant"]
)


@router.post('/{quiz_id}/{user_id}', status_code=status.HTTP_201_CREATED)
async def manage_participant(quiz_id: int, user_id: int, db: Session = Depends(get_db),
                             current_user: int = Depends(get_current_user)):

    existing_participant = db.query(Participant).filter(
        Participant.quiz_id == quiz_id, Participant.user_id == user_id).first()

    if existing_participant is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Perticipant already exist for the quiz")

    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    check_if_found(quiz, quiz_id, "quiz", "id")

    user = db.query(User).filter(User.id == user_id).first()
    check_if_found(user, user_id, "user", "id")

    new_participant = Participant(user_id=user_id, quiz_id=quiz_id)
    db.add(new_participant)
    db.commit()
    db.refresh(new_participant)
    return new_participant


@router.get('/', response_model=List[GetParticipant])
async def manage_participant(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    options = db.query(Participant).all()
    return options


@router.delete('/{participant_id}/{quiz_id}', status_code=status.HTTP_204_NO_CONTENT)
async def manage_participant(participant_id: int, quiz_id: int, db: Session = Depends(get_db),
                             current_user: int = Depends(get_current_user)):

    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    check_if_found(quiz, quiz_id, "quiz", "id")

    participant_query = db.query(Participant).filter(
        Participant.user_id == participant_id, Participant.quiz_id == quiz_id)

    participant_result = participant_query.first()

    if participant_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Participant with id {participant_id} was never added to the quiz")

    participant_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# A simple Quiz RestAPI created using FastAPI

# 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
