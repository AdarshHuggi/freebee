from database.db_connection import Base,engine
from sqlalchemy import create_engine, Column, Integer, Float,String,Boolean, ForeignKey, Text, TIMESTAMP,Date,func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


class UserDB(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, index=True, unique=True)
    email = Column(String, unique=True, nullable=True)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String)
    mobile_no =Column(String,nullable=False)
    is_activate = Column(String, default="active")
    reset_token = Column(String, nullable=True)





class Message(Base):
    __tablename__ = "customer_messages"

    message_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_to = Column(String, ForeignKey("customers.username", ondelete="SET NULL"))
    user_from = Column(String, ForeignKey("customers.username", ondelete="SET NULL"))
    content = Column(Text,nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

Base.metadata.create_all(engine)