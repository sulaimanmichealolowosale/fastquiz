from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text('CURRENT_TIMESTAMP'))
    quizzes = relationship("Quiz")


class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, nullable=False)
    user = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text('CURRENT_TIMESTAMP'))
    owner = relationship("User", foreign_keys=user, back_populates="quizzes")
    questions = relationship("Question")
    participants=relationship("Participant")


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, nullable=False)
    question_text = Column(String, nullable=False)
    quiz_id = Column(Integer, ForeignKey(
        "quizzes.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text('CURRENT_TIMESTAMP'))

    quiz = relationship("Quiz", foreign_keys=quiz_id,
                        back_populates="questions")
    options = relationship("Option")


class Option(Base):
    __tablename__ = "options"
    id = Column(Integer, primary_key=True, nullable=False)
    option_text = Column(String, nullable=False)
    question_id = Column(Integer, ForeignKey(
        "questions.id", ondelete="CASCADE"), nullable=False)
    is_correct = Column(Boolean, nullable=False, server_default=text('0'))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text('CURRENT_TIMESTAMP'))

    question = relationship("Question", foreign_keys=question_id,
                            back_populates="options")


class Participant(Base):
    __tablename__ = "participants"
    id = Column(Integer, primary_key=True, nullable=False)
    quiz_id = Column(Integer, ForeignKey(
        "quizzes.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))

    quiz = relationship("Quiz", foreign_keys=quiz_id,
                        back_populates="participants")
    user = relationship("User", foreign_keys=user_id)
