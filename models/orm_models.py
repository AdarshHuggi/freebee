from database.db_connection import Base,engine
from sqlalchemy import create_engine, Column, Integer, Float,String,Boolean, ForeignKey, Text, TIMESTAMP,Date,func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


class UserDB(Base):
    __tablename__ = 'users_chat_account'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, index=True, unique=True)
    email = Column(String, unique=True, nullable=True)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, nullable=False)


class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sending_to = Column(String, ForeignKey("users_chat_account.username"))
    username= Column(String, ForeignKey("users_chat_account.username"))
    content = Column(Text,nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

Base.metadata.create_all(engine)