import os
import pathlib
from fastapi import FastAPI, UploadFile
from typing import Union
from datetime import datetime
import pytz
from config import RAW_IMAGE_DIRECTORY,UPLOAD_DIR


def write_file_object_to_disk(path, file_obj):
    try:
        with open(path, "wb+") as output_file:
            output_file.write(file_obj.file.read())
        return True
    except Exception as e:
        print(f"Error while saving the file: {e}")
        return False

def save_file_upload_to_disk(file_obj, prefix='', save_dir='', sub_dir=''):
    if not save_dir:
        save_dir = UPLOAD_DIR

    if sub_dir:
        save_dir = os.path.join(save_dir, sub_dir)
        os.makedirs(save_dir, exist_ok=True)

    filename = file_obj.filename

    if prefix:
        filename = prefix + filename

    file_path = os.path.join(save_dir, filename)
    saved = write_file_object_to_disk(path=file_path, file_obj=file_obj)

    if saved:
        return file_path
    return None

def get_current_dt_str() -> str:
    return datetime.now(tz=pytz.timezone('Asia/Kolkata')).strftime("%Y%m%d_%H%M%S")

# Define a function to check file size
def check_file_size(file):
    max_size = 4 * 1024 * 1024  # 4 MB
    chunk = file.read(max_size)
    if not chunk:
        return False
    return True

