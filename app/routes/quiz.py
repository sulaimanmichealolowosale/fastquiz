from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AddQuiz, GetQuiz, GetQuestByQuiz
from app.models import User, Quiz
from app.utils import hash, check_if_found
from app.oauth2 import get_current_user
from typing import List

router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"]
)


@router.post('/', response_model=GetQuiz, status_code=status.HTTP_201_CREATED)
async def manage_quiz(quiz: AddQuiz, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    new_quiz = Quiz(**quiz.model_dump(), user=current_user.id)
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    return new_quiz


@router.get('/', response_model=List[GetQuiz])
async def manage_quiz(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    quizzes = db.query(Quiz).all()
    return quizzes


@router.get('/{id}', response_model=GetQuestByQuiz)
async def manage_quiz(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    quiz = db.query(Quiz).filter(Quiz.id == id).first()

    check_if_found(quiz, id, "quiz", "id")

    return quiz


@router.put('/{id}', response_model=GetQuiz, status_code=status.HTTP_201_CREATED)
async def manage_quiz(id: int, quiz: AddQuiz, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    quiz_query = db.query(Quiz).filter(Quiz.id == id)
    quiz_result = quiz_query.first()

    check_if_found(quiz_result, id, "quiz", "id")
    updated_quiz = quiz.model_dump()
    updated_quiz['user'] = id

    quiz_query.update(updated_quiz, synchronize_session=False)
    db.commit()
    return quiz_query.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def manage_quiz(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    quiz_query = db.query(Quiz).filter(Quiz.id == id)
    quiz_result = quiz_query.first()

    check_if_found(quiz_result, id, "quiz", "id")
    quiz_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
