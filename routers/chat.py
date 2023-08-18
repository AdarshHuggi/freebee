from datetime import datetime, timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from models.orm_models import Message
from schema.schemas import Token,MessageBase,User
from database.db_connection import Base,engine,get_db,SessionLocal
from auth.oauth2 import get_current_user,get_user

router = APIRouter(
    prefix="/messages",
    tags=['Message']
)





@router.post("/send_message/")
async def send_message(message: MessageBase,db: Session = Depends(get_db), current_user: str =Depends(get_current_user)):

    # Check if the receiver_id exists
    receiver_exists=get_user(message.sending_to)
   
    if not receiver_exists:
        raise HTTPException(status_code=404, detail="Receiver not present in the database")
    #try:
    new_msg = Message(username=current_user.username, **message.dict())
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    
    return {
        "username": current_user.username,
        "sending_to": message.sending_to,
        "content": message.content
    }
    # except Exception as e:
    #     db.rollback()
    #     raise HTTPException(status_code=500, detail="An error occurred while sending the message")
    # finally:
    #     db.close()
