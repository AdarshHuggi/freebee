from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from models.orm_models import Message
from schema.schemas import MessageBase
from database.db_connection import get_db
from auth.oauth2 import get_current_user,get_user

router = APIRouter(
    prefix="/messages",
    tags=['Message']
)


@router.post("/send_message/")
async def send_message(message: MessageBase,db:Session = Depends(get_db), current_user: str =Depends(get_current_user)):

    # Check if the receiver_id exists
    receiver_exists=get_user(message.send_to)
   
    if not receiver_exists:
        raise HTTPException(status_code=404, detail="Receiver not present in the database")
    try:
        new_msg = Message(from_to=current_user.username, **message.dict())
        db.add(new_msg)
        db.commit()
        db.refresh(new_msg)
        
        return {
            "from_to": current_user.username,
            "send_to": message.send_to,
            "content": message.content
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while sending the message")
    finally:
        db.close()



@router.delete("/messages/{message_id}/delete", response_model=dict)
def delete_message(message_id: int,db: Session = Depends(get_db),current_user: str =Depends(get_current_user)):
    # Get the message by its ID
    message = db.query(Message).filter(Message.message_id == message_id).first()

    if message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")

    # Delete the message from the database
    db.delete(message)
    db.commit()

    return {"message": "Message deleted successfully"}