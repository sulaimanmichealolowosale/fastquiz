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


@router.get('/{id}', response_model=GetOption)
async def manage_participant(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    option = db.query(Option).filter(Option.id == id).first()

    check_if_found(option, id, "option", "id")

    return option


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def manage_participant(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    option_query = db.query(Option).filter(Option.id == id)
    option_result = option_query.first()

    check_if_found(option_result, id, "option", "id")
    option_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



# A simple Quiz RestAPI created using FastAPI

# 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

