from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Response
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import secrets
from database.db_connection import SessionLocal,get_db
from models.orm_models import UserDB
from schema.reset_schema import ResetPasswordRequest,ResetPasswordToken
from auth.oauth2 import get_password_hash




router = APIRouter(prefix="/reset",tags=['reset password'])


# Replace these with your email and password details
EMAIL_SENDER = 'aaa.r.huggi@gmail.com'
EMAIL_PASSWORD = 'mzif rbmv tnyh edam'




# Generate a reset token (you can use a library like secrets.token_urlsafe)
# Generate a secure random token
reset_token = secrets.token_urlsafe(32)





@router.post("/forgot-password/")
async def forgot_password(request: ResetPasswordRequest,db:Session = Depends(get_db)):
    # Check if the email exists in the database
    db = SessionLocal()
    try:
        user_data = None
        user_data = db.query(UserDB).filter(UserDB.email ==request.email).first()
        print("email",user_data.email)
      
        user_data.reset_token = reset_token

        # Commit the changes to the database
        db.commit()
        db.close()
    

        if user_data is None:
            raise HTTPException(status_code=404, detail="Email not found")
            
    except Exception as e:
        print("failed to check_user_exist :",e)
    finally:
        db.close()


    # Send the reset password email
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = request.email
        msg['Subject'] = 'Reset Password'

        # You can customize the email message as needed
        message = f"Click the link below to reset your password:\n\n"
        message += f"Reset Link: https://localhost/reset/reset-password?token={reset_token}"

        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, request.email, msg.as_string())
        server.quit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

    return {"message": "Reset password email sent successfully"}




@router.post("/reset-password/")
async def reset_password(reset_request: ResetPasswordToken,db:Session = Depends(get_db)):
    # Find the user with the given reset token
    user_token = None
    user_token = db.query(UserDB).filter(UserDB.reset_token ==reset_request.token).first()
    new_password = get_password_hash(reset_request.password)
    user_token.hashed_password = new_password
    db.commit()
    db.close()

    if user_token is None:
        raise HTTPException(status_code=404, detail="Invalid or expired reset token")

    return {"message": "Password reset successful"}
