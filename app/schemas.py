from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CreateUser(BaseModel):
    username: str
    password: str


class GetUser(BaseModel):
    id: int
    username: str
    created_at: datetime

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    id: int


class AddQuiz(BaseModel):
    title: str


class GetQuiz(BaseModel):
    id: int
    title: str
    user: int
    created_at: datetime
    owner: Optional[GetUser] = {}

    class Config:
        from_attributes = True


class AddQuestion(BaseModel):
    question_text: str


class GetQuestion(AddQuestion):
    id: int
    question_text: str
    quiz_id: int
    created_at: datetime
    quiz: Optional[GetQuiz] = {}

    class Config:
        from_attributes = True


class AddOption(BaseModel):
    option_text: str
    is_correct: int


class GetOption(BaseModel):
    id: int
    option_text: str
    is_correct: int
    question_id: int
    created_at: datetime
    question: Optional[GetQuestion] = {}

    class Config:
        from_attributes = True


class GetParticipant(BaseModel):
    id:int
    quiz_id: int
    user_id: int

    quiz: Optional[GetQuiz] = {}
    user: Optional[GetUser] = {}

    class Config:
        from_attributes = True


class GetQuizByUser(GetUser):
    quizzes: List[GetQuiz]


class GetQuestByQuiz(GetQuiz):
    questions: List[GetQuestion]
    participants :List[GetParticipant]


class GetOptionByQuestion(GetQuestion):
    options: List[GetOption]
