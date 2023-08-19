from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import CreateUser, GetUser, GetQuizByUser
from app.models import User
from app.utils import hash, check_if_found
from app.oauth2 import get_current_user
from typing import List

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=GetUser)
async def manage_user(user: CreateUser, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.username == user.username).first()

    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"The user with username {user.username} already exist")

    hashed_password = hash(user.password)
    user.password = hashed_password

    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/', response_model=List[GetUser])
async def manage_user(db: Session = Depends(get_db), curent_user: int = Depends(get_current_user)):
    users = db.query(User).all()
    return users


@router.get('/{id}', response_model=GetQuizByUser)
async def manage_user(id: int, db: Session = Depends(get_db), curent_user: int = Depends(get_current_user)):
    user = db.query(User).filter(User.id == id).first()

    check_if_found(user, id, "user", "id")
    return user


@router.put('/{id}', response_model=GetUser, status_code=status.HTTP_201_CREATED)
async def manage_user(id: int, user: CreateUser, db: Session = Depends(get_db), curent_user: int = Depends(get_current_user)):
    user_query = db.query(User).filter(User.id == id)
    user_result = user_query.first()

    check_if_found(user_result, id, "user", "id")
    hashed_password = hash(user.password)
    user.password = hashed_password
    user_query.update(user.model_dump(), synchronize_session=False)
    db.commit()
    return user_query.first()


@router.delete('/{id}')
async def manage_user(id: int, db: Session = Depends(get_db), curent_user: int = Depends(get_current_user)):
    user_query = db.query(User).filter(User.id == id)
    user_result = user_query.first()

    check_if_found(user_result, id, "user", "id")
    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
