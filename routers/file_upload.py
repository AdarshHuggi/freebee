from fastapi import APIRouter,Depends,UploadFile
import os
import pathlib
from auth.oauth2 import get_current_user
from fastapi import FastAPI, UploadFile
from typing import Annotated
from schema.schemas import User,Create_User,UserResponse,UserUpdate
from config import RAW_IMAGE_DIRECTORY,UPLOAD_DIR


from utils.file_handle import get_current_dt_str,save_file_upload_to_disk,write_file_object_to_disk

router = APIRouter(prefix="/file_uploads",tags=['Uploads'])




@router.post("/upload/")
async def image_upload_handler(image: UploadFile, current_user: Annotated[User, Depends(get_current_user)]):
    print("current_user1",current_user.id)
    print("user_name1",current_user.username)

    # Check if the uploaded file is one of the allowed formats (jpeg, jpg, png)
    allowed_formats = {'.jpeg', '.jpg', '.png'}
    file_extension = pathlib.Path(image.filename).suffix.lower()
    if file_extension not in allowed_formats:
        return {"error": "Invalid file format. Allowed formats: jpeg, jpg, png"}

    filename_prefix = "{}_{}_".format(current_user.username,get_current_dt_str())
    image_path = save_file_upload_to_disk(file_obj=image, prefix=filename_prefix, save_dir=RAW_IMAGE_DIRECTORY)

    if image_path:
        return {"message": "Image uploaded successfully", "file_path": image_path}
    else:
        return {"error": "Failed to save the file"}
