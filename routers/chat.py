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
    receiver_exists=get_user(message.user_to)
    if not receiver_exists:
        raise HTTPException(status_code=404, detail="Receiver not present in the database")
    try:
        new_msg = Message(user_from=current_user.username, **message.dict())
        db.add(new_msg)
        db.commit()
        db.refresh(new_msg)
        
        return {
            "user_from": current_user.username,
            "user_to": message.user_to,
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

@router.get("/sent_items/")
def get_sent_items(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    # Get the username of the current user
    username = current_user.username

    # Retrieve sent items/messages for the current user
    sent_items = db.query(Message).filter(Message.user_from == username).all()

    if not sent_items:
        return {"message": "No sent messages found"}

    # You may want to serialize the sent_items to JSON or another suitable format
    # For simplicity, we assume Message has a 'to_user' field for the recipient's username
    serialized_items = [{"message_id": item.message_id, "content": item.content, "to_user": item.user_to} for item in sent_items]

    return {"sent_items": serialized_items}



@router.get("/received_items/")
def get_received_items(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    # Get the username of the current user
    username = current_user.username

    # Retrieve sent items/messages for the current user
    received_items = db.query(Message).filter(Message.user_to == username).all()

    if not received_items:
        return {"message": "No received messages found"}

    # You may want to serialize the sent_items to JSON or another suitable format
    # For simplicity, we assume Message has a 'to_user' field for the recipient's username
    serialized_items = [{"message_id": item.message_id, "content": item.content, "from_user": item.user_from} for item in received_items]

    return {"received_items": serialized_items}
