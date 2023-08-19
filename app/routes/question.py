from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AddQuestion, GetQuestion, GetOptionByQuestion
from app.models import User, Quiz, Question
from app.utils import hash, check_if_found
from app.oauth2 import get_current_user
from typing import List

router = APIRouter(
    prefix="/question",
    tags=["Question"]
)


@router.post('/{id}', response_model=GetQuestion, status_code=status.HTTP_201_CREATED)
async def manage_question(id: int, question: AddQuestion, db: Session = Depends(get_db),
                          current_user: int = Depends(get_current_user)):

    quiz = db.query(Quiz).filter(Quiz.id == id).first()
    check_if_found(quiz, id, "quiz", "id")

    new_question = Question(**question.model_dump(), quiz_id=id)
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question


@router.get('/', response_model=List[GetQuestion])
async def manage_question(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    quizzes = db.query(Question).all()
    return quizzes


@router.get('/{id}', response_model=GetOptionByQuestion)
async def manage_question(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    question = db.query(Question).filter(Question.id == id).first()

    check_if_found(question, id, "question", "id")

    return question


@router.put('/{id}', response_model=GetQuestion, status_code=status.HTTP_201_CREATED)
async def manage_question(id: int, question: AddQuestion, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    question_query = db.query(Question).filter(Question.id == id)
    question_result = question_query.first()

    check_if_found(question_result, id, "question", "id")
    updated_question = question.model_dump()
    updated_question['quiz_id'] = question_result.quiz_id

    question_query.update(updated_question, synchronize_session=False)
    db.commit()
    return question_query.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def manage_question(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    question_query = db.query(Question).filter(Question.id == id)
    question_result = question_query.first()

    check_if_found(question_result, id, "question", "id")
    question_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
