from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Response
from auth.oauth2 import get_current_user,get_password_hash
from schema.schemas import User,Create_User,UserResponse
from models.orm_models import UserDB
from database.db_connection import get_db


router = APIRouter(prefix="/users",tags=['Users'])

@router.get("/current_user_data/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    print("current_user",current_user.id)
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