from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AddQuestion, GetQuestion, AddOption, GetOption
from app.models import User, Quiz, Question, Option
from app.utils import hash, check_if_found
from app.oauth2 import get_current_user
from typing import List

router = APIRouter(
    prefix="/option",
    tags=["Option"]
)


@router.post('/{id}', response_model=GetOption, status_code=status.HTTP_201_CREATED)
async def manage_option(id: int, option: AddOption, db: Session = Depends(get_db),
                        current_user: int = Depends(get_current_user)):

    question = db.query(Question).filter(Question.id == id).first()
    check_if_found(question, id, "question", "id")

    new_option = Option(**option.model_dump(), question_id=id)
    db.add(new_option)
    db.commit()
    db.refresh(new_option)
    return new_option


@router.get('/', response_model=List[GetOption])
async def manage_option(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    options = db.query(Option).all()
    return options


@router.get('/{id}', response_model=GetOption)
async def manage_option(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    option = db.query(Option).filter(Option.id == id).first()

    check_if_found(option, id, "option", "id")

    return option


@router.put('/{id}', response_model=GetOption, status_code=status.HTTP_201_CREATED)
async def manage_option(id: int, option: AddOption, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    option_query = db.query(Option).filter(Option.id == id)
    option_result = option_query.first()

    check_if_found(option_result, id, "option", "id")
    updated_option = option.model_dump()
    updated_option['question_id'] = option_result.question_id

    option_query.update(updated_option, synchronize_session=False)
    db.commit()
    return option_query.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def manage_option(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    option_query = db.query(Option).filter(Option.id == id)
    option_result = option_query.first()

    check_if_found(option_result, id, "option", "id")
    option_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
