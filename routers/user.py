from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Response
from auth.oauth2 import get_current_user,get_password_hash
from schema.schemas import User,Create_User,UserResponse,UserUpdate
from models.orm_models import UserDB
from database.db_connection import get_db
import random
import smtplib


router = APIRouter(prefix="/users",tags=['Users'])

@router.get("/current_user_data/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    print("current_user",current_user.id)
    print("user_name",current_user.username)
    return current_user



@router.post("/create_user", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user_data: Create_User, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user_data.password)
    new_user_data = user_data.dict()
    del new_user_data['password']  # Remove the 'password' field
    new_user = UserDB(**new_user_data, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    user_response = UserResponse(**new_user.__dict__)
    return user_response




@router.delete("/user/delete", response_model=dict)
def delete_user(db:Session = Depends(get_db), current_user: str =Depends(get_current_user)):
    # Get the user by their ID
    user = db.query(UserDB).filter(UserDB.username == current_user.username).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Delete the user from the database
    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}