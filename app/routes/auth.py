from fastapi import APIRouter, Depends, status, HTTPException, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.utils import verify_password
from app.oauth2 import create_access_token, verify_access_token
from datetime import timedelta


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post('/')
async def auth(response: Response, login_details: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_query = db.query(User).filter(User.username == login_details.username)
    user_result = user_query.first()

    if user_result is None or not verify_password(login_details.password, user_result.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # response.delete_cookie("refresh_token")
    access_token = create_access_token(data={"id": user_result.id})
    refresh_token = create_access_token(
        data={"id": user_result.id}, expire_time=timedelta(days=1))
    response.set_cookie("refresh_token", refresh_token, httponly=True)
    response.set_cookie("access_token", access_token, httponly=True)

    return {
        "username": login_details.username,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token-type": "Bearer"
    }


@router.post('/refresh')
async def auth(response: Response, refresh_token: str = Cookie(default=None), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                          detail=f"Could not validate credentials", headers={"www-authenticate": "bearer"})
    payload = verify_access_token(
        refresh_token, credentials_exception)
    
    user = db.query(User).filter(User.id == payload.id).first()
    
    access_token = create_access_token(data={"id": payload.id})
    # response.delete_cookie("access_token")
    response.set_cookie("access_token", access_token,  httponly=True)
    return {"access_token": access_token, "username": user.username}


